from __future__ import annotations

from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Static


class Header(Static):
    DEFAULT_CSS = """
    Header {
        height: auto;
        padding-top: 1;
        padding-left: 1;
        padding-right: 1;
    }

    Header > Static {
        padding-left: 2;
        content-align: center middle;
    }

    Header > #title {
        color: $accent-lighten-2;
        text-style: bold
    }

    Header > #title-separator {
        color: $surface-lighten-2;
        text-style: dim;
    }

    Header > #sub-title {
        color: $accent-lighten-2;
        text-style: dim;
    }

    Header > #divider {
        color: $surface-lighten-2;
        text-style: dim;
    }

    """

    def __init__(self, title: str, sub_title: str = "", id: str | None = None, classes: str | None = None) -> None:
        super().__init__(id=id, classes=classes)
        self._title = title
        self._sub_title = sub_title
        self._text_width = max(len(title), len(sub_title)) + 2

    def compose(self) -> ComposeResult:
        yield Static(Text(self._title), id="title")
        yield Static(
            Text("─" * self._text_width),
            id="title-separator",
        )
        if self._sub_title:
            yield Static(Text(self._sub_title), id="sub-title")

        yield Static(
            Text("─" * self._text_width),
            id="divider",
        )
