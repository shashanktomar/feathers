from __future__ import annotations

from typing import Self, cast

from rich.console import Console, RenderableType
from rich.highlighter import Highlighter, ReprHighlighter
from rich.measure import Measurement
from rich.pretty import Pretty
from rich.protocol import is_renderable
from rich.segment import Segment
from rich.text import Text
from textual._cache import LRUCache
from textual.geometry import Size
from textual.scroll_view import ScrollView
from textual.strip import Strip


class TextView(ScrollView):
    """A widget for logging text."""

    DEFAULT_CSS = """
    TextLog{
        background: $surface;
        color: $text;
        overflow-y: scroll;
    }
    """

    max_lines: int | None = None
    min_width: int = 78
    wrap: bool = False
    highlight: bool = False
    markup: bool = False
    auto_scroll: bool = True

    def __init__(
        self,
        *,
        max_lines: int | None = None,
        min_width: int = 78,
        wrap: bool = False,
        highlight: bool = False,
        markup: bool = False,
        auto_scroll: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Create a TextLog widget.

        Args:
            max_lines: Maximum number of lines in the log or `None` for no maximum.
            min_width: Minimum width of renderables.
            wrap: Enable word wrapping (default is off).
            highlight: Automatically highlight content.
            markup: Apply Rich console markup.
            auto_scroll: Enable automatic scrolling to end.
            name: The name of the text log.
            id: The ID of the text log in the DOM.
            classes: The CSS classes of the text log.
            disabled: Whether the text log is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.max_lines = max_lines
        """Maximum number of lines in the log or `None` for no maximum."""
        self._start_line: int = 0
        self.lines: list[Strip] = []
        self._line_cache: LRUCache[tuple[int, int, int, int], Strip]
        self._line_cache = LRUCache(1024)
        self.max_width: int = 0
        self.min_width = min_width
        """Minimum width of renderables."""
        self.wrap = wrap
        """Enable word wrapping."""
        self.highlight = highlight
        """Automatically highlight content."""
        self.markup = markup
        """Apply Rich console markup."""
        self.auto_scroll = auto_scroll
        """Automatically scroll to the end on write."""
        self.highlighter = ReprHighlighter()

    def notify_style_update(self) -> None:
        self._line_cache.clear()

    def _extract_lines(
        self,
        content: RenderableType | object,
        console: Console,
        width: int | None = None,
        highlighter: Highlighter | None = None,
        markup: bool = False,
        wrap: bool = False,
        expand: bool = False,
        shrink: bool = True,
    ) -> list[Strip] | None:
        renderable: RenderableType
        if not is_renderable(content):
            renderable = Pretty(content)
        else:
            if isinstance(content, str):
                if markup:
                    renderable = Text.from_markup(content)
                else:
                    renderable = Text(content)
                if highlighter is not None:
                    renderable = highlighter(renderable)
            else:
                renderable = cast(RenderableType, content)

        render_options = console.options

        if isinstance(renderable, Text) and not wrap:
            render_options = render_options.update(overflow="ignore", no_wrap=True)

        render_width = Measurement.get(console, render_options, renderable).maximum
        if width:
            if expand and render_width < width:
                render_width = width
            if shrink and render_width > width:
                render_width = width

        segments = console.render(renderable, render_options.update_width(render_width))
        lines = list(Segment.split_lines(segments))
        if not lines:
            return None

        strips = Strip.from_lines(lines)
        for strip in strips:
            strip.adjust_cell_length(render_width)
        return strips

    def write(
        self,
        content: RenderableType | object,
        width: int | None = None,
        expand: bool = False,
        shrink: bool = True,
        scroll_end: bool | None = None,
    ) -> Self:
        """Write text or a rich renderable.

        Args:
            content: Rich renderable (or text).
            width: Width to render or `None` to use optimal width.
            expand: Enable expand to widget width, or `False` to use `width`.
            shrink: Enable shrinking of content to fit width.
            scroll_end: Enable automatic scroll to end, or `None` to use `self.auto_scroll`.

        Returns:
            The `TextLog` instance.
        """

        container_width = self.scrollable_content_region.width if width is None else width
        self.log("============in write==============>")
        self.log(self.scrollable_content_region)
        self.log(self.content_size)
        self.log(self.size)
        strips = self._extract_lines(
            content,
            self.app.console,
            container_width,
            self.highlighter,
            self.markup,
            self.wrap,
            expand,
            shrink,
        )

        if not strips:
            return self
        self.lines.extend(strips)

        self.max_width = max(
            self.max_width,
            max(sum([segment.cell_length for segment in strip]) for strip in strips),
        )

        if self.max_lines is not None and len(self.lines) > self.max_lines:
            self._start_line += len(self.lines) - self.max_lines
            self.refresh()
            self.lines = self.lines[-self.max_lines :]
        self.virtual_size = Size(self.max_width, len(self.lines))

        auto_scroll = self.auto_scroll if scroll_end is None else scroll_end
        if auto_scroll:
            self.scroll_end(animate=False)

        return self

    def on_mount(self):
        self.log("============in on_mount==============>")
        self.log(self.scrollable_content_region)
        self.log(self.content_size)
        self.log(self.size)
        return super().on_mount()

    def on_resize(self):
        self.log("============in on_resize==============>")
        self.log(self.scrollable_content_region)
        self.log(self.content_size)
        self.log(self.size)

    def on_show(self):
        self.log("============in on_show==============>")
        self.log(self.scrollable_content_region)
        self.log(self.content_size)
        self.log(self.size)

    def clear(self) -> Self:
        """Clear the text view.

        Returns:
            The `TextView` instance.
        """
        self.lines.clear()
        self._line_cache.clear()
        self._start_line = 0
        self.max_width = 0
        self.virtual_size = Size(0, 0)
        self.refresh()
        return self

    def render_line(self, y: int) -> Strip:
        scroll_x, scroll_y = self.scroll_offset
        line = self._render_line(scroll_y + y, scroll_x, self.size.width)
        strip = line.apply_style(self.rich_style)
        return strip

    def _render_line(self, y: int, scroll_x: int, width: int) -> Strip:
        if y >= len(self.lines):
            return Strip.blank(width, self.rich_style)

        key = (y + self._start_line, scroll_x, width, self.max_width)
        if key in self._line_cache:
            return self._line_cache[key]

        line = (
            self.lines[y]
            .adjust_cell_length(max(self.max_width, width), self.rich_style)
            .crop(scroll_x, scroll_x + width)
        )

        self._line_cache[key] = line
        return line
