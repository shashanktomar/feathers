from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar

from rich.containers import Lines
from rich.repr import Result
from rich.text import Text
from textual.binding import Binding, BindingType
from textual.events import Blur, Mount
from textual.geometry import Offset, Size
from textual.reactive import reactive
from textual.scroll_view import ScrollView

from feathers.text import Block


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
    _cursor_visible = reactive(True)

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialise the `Input` widget.

        Args:
            name: Optional name for the input widget.
            id: Optional ID for the widget.
            classes: Optional initial classes for the widget.
            disabled: Whether the input is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

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

    def watch_cursor_position(self, cursor_position: int) -> None:
        """
        Notes: Here we take care of the scrolling.
        """
        pass

    def validate_cursor_position(self, cursor_position: Offset) -> Offset:
        lines = self.visible_lines()
        content_w, content_h = self.content_size
        y = min(cursor_position.y, len(lines) - 1, content_h - 1)
        line = lines[y]
        x = min(cursor_position.x, line.cell_len - 1, content_w - 1)
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
