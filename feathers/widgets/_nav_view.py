from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar

from rich.repr import Result
from rich.style import Style
from textual.binding import Binding, BindingType
from textual.events import Blur, Focus
from textual.geometry import Offset
from textual.message import Message
from textual.reactive import reactive
from textual.scroll_view import ScrollView
from textual.strip import Strip


class NavigableView(ScrollView, can_focus=True):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("left, h", "cursor_left", "cursor left", show=False),
        Binding("down, j", "cursor_down", "cursor down", show=False),
        Binding("up, k", "cursor_up", "cursor up", show=False),
        Binding("right, l", "cursor_right", "cursor right", show=False),
    ]

    COMPONENT_CLASSES: ClassVar[set[str]] = {"navigation-box--cursor"}
    """
    | Class | Description |
    | :- | :- |
    | `navigation-box--cursor` | Target the cursor. |
    """

    DEFAULT_CSS = """
    .navigation-box--cursor {
        background: $surface;
        color: $text;
        text-style: reverse;
    }
    """

    cursor_position: reactive[Offset] = reactive(Offset(0, 0))
    _cursor_visible = reactive(True)

    class Changed(Message, bubble=False):
        """Posted when the cursor value changes.

        Can be handled using `on_cursor_view_changed` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            value: The value that the cursor was changed to. It is the offset of the cursor
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: NavigableView, value: Offset) -> None:
            super().__init__()
            self.cursor_view: NavigableView = cursor_view
            self.value: Offset = value
            self._content_size = self.cursor_view.content_size

        @property
        def control(self) -> NavigableView:
            """Alias for self.cursor_view."""
            return self.cursor_view

    class SeekBottom(Message, bubble=False):
        """Posted when the cursor is pushed beyond bottom of the available content height.

        Can be handled using `on_cursor_view_seek_bottom` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: NavigableView) -> None:
            super().__init__()
            self.cursor_view: NavigableView = cursor_view

    class SeekTop(Message, bubble=False):
        """Posted when the cursor is pushed beyond top of the availalbe content height.

        Can be handled using `on_cursor_view_seek_top` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: NavigableView) -> None:
            super().__init__()
            self.cursor_view: NavigableView = cursor_view

    class SeekLeft(Message, bubble=False):
        """Posted when the cursor is pushed beyond left of the availalbe content width.

        Can be handled using `on_cursor_view_seek_left` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: NavigableView) -> None:
            super().__init__()
            self.cursor_view: NavigableView = cursor_view

    class SeekRight(Message, bubble=False):
        """Posted when the cursor is pushed beyond right of the availalbe content width.

        Can be handled using `on_cursor_view_seek_right` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: NavigableView) -> None:
            super().__init__()
            self.cursor_view: NavigableView = cursor_view

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialise the `Input` widget.

        Args:
            mode: A mode in which cursor view should operate.
            name: Optional name for the input widget.
            id: Optional ID for the widget.
            classes: Optional initial classes for the widget.
            disabled: Whether the input is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    @abstractmethod
    def lines_count(self) -> int:
        pass

    @abstractmethod
    def line_at(self, y: int) -> Strip:
        pass

    def add_cursor_to_line(self, y: int, line: Strip) -> Strip:
        if self.cursor_position.y != y:
            return line

        cursor_style = self.get_component_rich_style("navigation-box--cursor")

        if self._cursor_visible and self.has_focus:
            cursor_pos = min(self.cursor_position.x, line.cell_length)
            return self._add_style_to_strip(line, cursor_pos, cursor_style)
        return line

    def _add_style_to_strip(self, line: Strip, pos: int, style: Style) -> Strip:
        strips = line.divide([pos, pos + 1, line.cell_length])
        if len(strips) < 2:
            return line
        changed_strips = list(strips)
        cursor_strip = strips[1]
        changed_strips[1] = cursor_strip.apply_style(style)
        return Strip.join(changed_strips)

    # def add_cursor(self) -> Lines:
    #     lines = self.visible_lines()
    #     if len(lines) > self.cursor_position.y:
    #         self.cursor_position = self.validate_cursor_position(self.cursor_position)
    #
    #     y = self.cursor_position.y
    #     cursor_style = self.get_component_rich_style("navigation-box--cursor")
    #
    #     focused_line = lines[y].copy()
    #     if self._cursor_visible and self.has_focus:
    #         cursor_pos = min(self.cursor_position.x, focused_line.cell_len)
    #         focused_line.stylize(cursor_style, cursor_pos, cursor_pos + 1)
    #     return Lines(lines[:y] + [focused_line] + lines[y + 1 :])

    # def _position_to_cell(self, position: int) -> int:
    #     """Convert an index within the value to cell position."""
    #     cell_offset = cell_len(self.value[:position])
    #     return cell_offset
    #
    # @property
    # def _cursor_offset(self) -> int:
    #     """The cell offset of the cursor."""
    #     offset = self._position_to_cell(self.cursor_position)
    #     if self._cursor_at_end:
    #         offset += 1
    #     return offset

    def watch_cursor_position(self, cursor_position: Offset) -> None:
        self.post_message(self.Changed(self, cursor_position))

    def validate_cursor_position(self, cursor_position: Offset) -> Offset:
        content_w, content_h = self.content_size
        if cursor_position.y == content_h:
            self.post_message(self.SeekBottom(self))
        if cursor_position.y < 0:
            self.post_message(self.SeekTop(self))
        if cursor_position.x < 0:
            self.post_message(self.SeekLeft(self))
        if cursor_position.x == content_w:
            self.post_message(self.SeekRight(self))

        y = min(cursor_position.y, self.lines_count() - 1, content_h - 1)
        line = self.line_at(y)
        x = min(cursor_position.x, line.cell_length - 1, content_w)
        pos = Offset(x, y)
        return pos.clamped

    def on_navigable_view_seek_bottom(self, _: NavigableView.SeekBottom) -> None:
        self.scroll_down(animate=False)

    def on_navigable_view_seek_top(self, _: NavigableView.SeekTop) -> None:
        self.scroll_up(animate=False)

    def on_navigable_view_seek_left(self, _: NavigableView.SeekBottom) -> None:
        self.scroll_left(animate=False)

    def on_navigable_view_seek_right(self, _: NavigableView.SeekTop) -> None:
        self.scroll_right(animate=False)

    def _on_blur(self, _: Blur) -> None:
        self._cursor_visible = False

    def _on_focus(self, _: Focus) -> None:
        self._cursor_visible = True

    def action_cursor_left(self) -> None:
        """Move the cursor one position to the left."""
        self.cursor_position += Offset(-1, 0)

    def action_cursor_right(self) -> None:
        """Move the cursor one position to the right."""
        self.cursor_position += Offset(1, 0)

    def action_cursor_up(self) -> None:
        """Move the cursor one position upwards."""
        self.cursor_position += Offset(0, -1)

    def action_cursor_down(self) -> None:
        """Move the cursor one position downwards."""
        self.cursor_position += Offset(0, 1)

    def __rich_repr__(self) -> Result:
        yield from super().__rich_repr__()
        yield "cursor_position", self.cursor_position
        yield "_cursor_visible", self._cursor_visible
