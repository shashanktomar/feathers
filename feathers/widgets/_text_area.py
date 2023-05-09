from __future__ import annotations

from typing import ClassVar

from rich.console import Console, ConsoleOptions, RenderableType, RenderResult
from rich.highlighter import Highlighter
from rich.repr import Result
from rich.segment import Segment
from rich.text import Text
from textual.app import events
from textual.binding import BindingType
from textual.geometry import Offset
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget


class _TextAreaRenderable:
    """Render the text area content."""

    def __init__(self, parent: TextArea) -> None:
        self.parent = parent
        self.value = parent.value

    @property
    def _value(self) -> Text:
        """Value rendered as text."""
        text = Text(self.value, no_wrap=True, overflow="ignore")
        return text

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        parent = self.parent
        result = self._value
        width = parent.content_size.width
        segments = list(result.render(console))
        line_length = Segment.get_line_length(segments)
        if line_length < width:
            segments = Segment.adjust_line_length(segments, width)
            line_length = width
        yield from segments


class TextArea(Widget, can_focus=True):
    """A text area widget."""

    BINDINGS: ClassVar[list[BindingType]] = []

    COMPONENT_CLASSES: ClassVar[set[str]] = {"textarea--cursor", "textarea--placeholder"}
    """
    | Class | Description |
    | :- | :- |
    | `textarea--cursor` | Target the cursor. |
    | `textarea--placeholder` | Target the placeholder text (when it exists). |
    """

    DEFAULT_CSS = """
    TextArea {
        background: $boost;
        color: $text;
        padding: 0 2;
        border: none;
        border-left: $boost-darken-1 ;
        width: 100%;
        height: 3;
        min-height: 1;
    }
    TextArea:focus {
        border: none;
        border-left: white;
    }
    TextArea>.textarea--cursor {
        background: $surface;
        color: $text;
        text-style: reverse;
    }
    TextArea>.textarea--placeholder {
        color: $text-disabled;
    }
    """

    value: reactive[list[str]] = reactive([""], init=False)
    placeholder = reactive("")
    cursor_position: reactive[Offset] = reactive(Offset(0, 0))

    class Changed(Message, bubble=True):
        """Posted when the value changes.

        Can be handled using `on_input_changed` in a subclass of `TextArea` or in a parent
        widget in the DOM.

        Attributes:
            value: The value that the input was changed to. It is an iterable of lines
            text_area: The `TextArea` widget that was changed.
        """

        def __init__(self, text_area: TextArea, value: str) -> None:
            super().__init__()
            self.text_area: TextArea = text_area
            self.value: str = value

        @property
        def control(self) -> TextArea:
            """Alias for self.text_area."""
            return self.text_area

    class Submitted(Message, bubble=True):
        """Posted when the text in `TextArea` is submitted.

        Can be handled using `on_input_submitted` in a subclass of `TextArea` or in a
        parent widget in the DOM.

        Attributes:
            value: The value of the `TextArea` being submitted.
            text_area: The `TextArea` widget that is being submitted.
        """

        def __init__(self, text_area: TextArea, value: str) -> None:
            super().__init__()
            self.text_area: TextArea = text_area
            self.value: str = value

        @property
        def control(self) -> TextArea:
            """Alias for self.text_area."""
            return self.text_area

    def __init__(
        self,
        value: list[str] | None = None,
        placeholder: str = "",
        highlighter: Highlighter | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialise the `TextArea` widget.

        Args:
            value: An optional default value for the input.
            placeholder: Optional placeholder text for the input.
            highlighter: An optional highlighter for the input.
            name: Optional name for the input widget.
            id: Optional ID for the widget.
            classes: Optional initial classes for the widget.
            disabled: Whether the input is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        if value is not None:
            self.value = value
        self.placeholder = placeholder
        # self.highlighter = highlighter

    def __rich_repr__(self) -> Result:
        yield from super().__rich_repr__()
        yield "value", self.value
        yield "cursor_position", self.cursor_position
        # yield "input_scroll_offset", self.input_scroll_offset
        # yield "view_position", self.view_position
        # yield "complete", self.complete
        # yield "width", self.width
        # yield "_cursor_visible", self._cursor_visible
        # yield "max_size", self.max_size

    async def watch_value(self, value: str) -> None:
        self.post_message(self.Changed(self, value))

    def _render_placeholder(self) -> RenderableType:
        placeholder = Text(self.placeholder, justify="left")
        placeholder.stylize(self.get_component_rich_style("textarea--placeholder"))
        return placeholder

    def render(self) -> RenderableType:
        # self.view_position = self.view_position
        if not self.value:
            return self._render_placeholder()
        return _TextAreaRenderable(self)

    def get_content_width(self, container: Size, viewport: Size) -> int:
        return 10

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        return 1

    async def _on_key(self, event: events.Key) -> None:
        # Do key bindings first
        if await self.handle_key(event):
            event.prevent_default()
            event.stop()
            return
        elif event.is_printable:
            event.stop()
            assert event.character is not None
            self.insert_text_at_cursor(event.character)
            event.prevent_default()
        elif event.key == "enter":
            event.stop()
            self.insert_text_at_cursor("\n")
            event.prevent_default()

    def insert_text_at_cursor(self, text: str) -> None:
        """Insert new text at the cursor, move the cursor to the end of the new text.

        Args:
            text: New text to insert.
        """
        if self.cursor_position > len(self.value):
            self.value += text
            self.cursor_position = len(self.value)
        else:
            value = self.value
            before = value[: self.cursor_position]
            after = value[self.cursor_position :]
            self.value = f"{before}{text}{after}"
            self.cursor_position += len(text)

    async def action_submit(self) -> None:
        """Handle a submit action"""
        self.post_message(self.Submitted(self, self.value))
