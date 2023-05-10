from __future__ import annotations

import random

from rich.console import RenderableType
from rich.containers import Lines
from rich.text import Text
from textual.app import App, ComposeResult

from feathers.widgets import CursorView


class NavigableBox(CursorView, can_focus=True):
    DEFAULT_CSS = """
    NavigableBox {
        width: 1fr;
        height: 1fr;
        layout: vertical;
        overflow: auto auto;
    }
    """

    def __init__(
        self,
        text: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self._text = Text(text)
        self._lines = None

    # def visible_block(self) -> Block:
    #     s = Segment("Hi There")
    #     return Block([Strip([s])])

    def on_cursor_view_changed(self, event: CursorView.Changed) -> None:
        self.log("------------->")
        self.log(event)

    def on_cursor_view_seekbottom(self, event: CursorView.SeekBottom) -> None:
        self.log("------------->")
        self.log(event)

    def on_cursor_view_seek_top(self, event: CursorView.SeekBottom) -> None:
        self.log("------------->")
        self.log(event)

    def visible_lines(self) -> Lines:
        if self._lines is None:
            self._lines = self._text.split()
        return self._lines

    def render(self) -> RenderableType:
        lines = self.add_cursor()
        return lines


class NavigableApp(App):
    CSS_PATH = "navigable.css"

    text = "Why do programmers prefer dark mode? Because light attracts bugs"

    def compose(self) -> ComposeResult:
        long = "\n".join([self.text[: random.randint(1, len(self.text))] for _ in range(10)])
        very_long = "\n".join([self.text[: random.randint(1, len(self.text))] for _ in range(60)])

        yield NavigableBox(self.text, classes="box")
        yield NavigableBox(long, classes="box")
        yield NavigableBox(very_long, classes="box")
        yield NavigableBox((self.text * 4 + "\n") * 40, classes="box")


if __name__ == "__main__":
    app = NavigableApp()
    app.run()
