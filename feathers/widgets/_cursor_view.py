from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar, Literal

from rich.containers import Lines
from rich.repr import Result
from textual.binding import Binding, BindingType
from textual.events import Blur, Mount
from textual.geometry import Offset
from textual.message import Message
from textual.reactive import reactive
from textual.scroll_view import ScrollView

from feathers.text import Block
from feathers.utils import friendly_list

CursorMode = Literal["view", "edit"]
"""The names of the valid cursor modes.

These are the modes that can be used with a [`Cursor`][feathers.widgets.CursorView].
"""

_VALID_CURSOR_MODES = {"view", "edit"}


class InvalidCursorMode(Exception):
    """Exception raised if an invalid cursor mode is used."""


class CursorView(ScrollView, can_focus=True):
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
    cursor_blink = reactive(True)
    mode: reactive[CursorMode] = reactive[CursorMode]("view")
    """This decide how the cursor behave, it can be in view or in edit mode"""
    _cursor_visible = reactive(True)

    class Changed(Message, bubble=False):
        """Posted when the cursor value changes.

        Can be handled using `on_cursor_view_changed` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            value: The value that the cursor was changed to. It is the offset of the cursor
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: CursorView, value: Offset) -> None:
            super().__init__()
            self.cursor_view: CursorView = cursor_view
            self.value: Offset = value
            self._content_size = self.cursor_view.content_size

        @property
        def control(self) -> CursorView:
            """Alias for self.cursor_view."""
            return self.cursor_view

    class SeekBottom(Message, bubble=False):
        """Posted when the cursor is pushed beyond bottom of the available content height.

        Can be handled using `on_cursor_view_seek_bottom` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: CursorView) -> None:
            super().__init__()
            self.cursor_view: CursorView = cursor_view

    class SeekTop(Message, bubble=False):
        """Posted when the cursor is pushed beyond top of the availalbe content height.

        Can be handled using `on_cursor_view_seek_top` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: CursorView) -> None:
            super().__init__()
            self.cursor_view: CursorView = cursor_view

    class SeekLeft(Message, bubble=False):
        """Posted when the cursor is pushed beyond left of the availalbe content width.

        Can be handled using `on_cursor_view_seek_left` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: CursorView) -> None:
            super().__init__()
            self.cursor_view: CursorView = cursor_view

    class SeekRight(Message, bubble=False):
        """Posted when the cursor is pushed beyond right of the availalbe content width.

        Can be handled using `on_cursor_view_seek_right` in a subclass of `CursorView` or in a parent
        widget in the DOM.

        Attributes:
            cursor_view: Reference to the originating parent CursorView
        """

        def __init__(self, cursor_view: CursorView) -> None:
            super().__init__()
            self.cursor_view: CursorView = cursor_view

    def __init__(
        self,
        mode: CursorMode = "view",
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
        self.mode = mode

    @abstractmethod
    def visible_block(self) -> Block:
        pass

    @abstractmethod
    def visible_lines(self) -> Lines:
        pass

    def is_cursor_on_line(self, y: int) -> bool:
        return y == self.cursor_position.y

    def add_cursor(self) -> Lines:
        lines = self.visible_lines()
        if len(lines) > self.cursor_position.y:
            self.cursor_position = self.validate_cursor_position(self.cursor_position)

        y = self.cursor_position.y
        cursor_style = self.get_component_rich_style("navigation-box--cursor")

        focused_line = lines[y].copy()
        if self._cursor_visible and self.has_focus:
            cursor_pos = min(self.cursor_position.x, focused_line.cell_len)
            focused_line.stylize(cursor_style, cursor_pos, cursor_pos + 1)
        return Lines(lines[:y] + [focused_line] + lines[y + 1 :])

    def validate_mode(self, mode: str) -> str:
        """Validate the mode."""
        if mode not in _VALID_CURSOR_MODES:
            raise InvalidCursorMode(f"Valid cursor modes are {friendly_list(_VALID_CURSOR_MODES)}")
        return mode

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
    #
    # @property
    # def _cursor_at_end(self) -> bool:
    #     """Flag to indicate if the cursor is at the end"""
    #     return self.cursor_position >= len(self.value)
    #
    # def validate_cursor_position(self, cursor_position: int) -> int:
    #     return min(max(0, cursor_position), len(self.value))

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

        lines = self.visible_lines()
        y = min(cursor_position.y, len(lines) - 1, content_h - 1)
        line = lines[y]
        x = min(cursor_position.x, line.cell_len - 1, content_w)
        pos = Offset(x, y)
        return pos.clamped

    def _toggle_cursor(self) -> None:
        """Toggle visibility of cursor."""
        self._cursor_visible = not self._cursor_visible

    def _on_mount(self, _: Mount) -> None:
        self.blink_timer = self.set_interval(
            0.5,
            self._toggle_cursor,
            pause=not (self.cursor_blink and self.has_focus),
        )

    def _on_blur(self, _: Blur) -> None:
        self.blink_timer.pause()

    # def _on_focus(self, _: Focus) -> None:
    #     self.cursor_position = len(self.value)
    #     if self.cursor_blink:
    #         self.blink_timer.resume()

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
        yield "cursor_blink", self.cursor_blink
        yield "cursor_position", self.cursor_position
        yield "_cursor_visible", self._cursor_visible
