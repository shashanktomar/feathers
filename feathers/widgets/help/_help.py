from __future__ import annotations

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import ContentSwitcher

from ._base import BaseHelp
from ._long_help import LongHelp
from ._models import HelpEntry
from ._short_help import ShortHelp


class Help(Widget):
    """A single and multi line mode help widget to display key bindings"""

    DEFAULT_CSS = """
    Help {
        dock: bottom;
        width: 100w;
        min-height: 1;
        height: auto;
    }

    Help > ContentSwitcher {
        height: auto;
    }
    """

    def __init__(
        self,
        toggle_key: HelpEntry = HelpEntry("?", "toggle help", True),
        short_help_separator: str = " • ",
        short_help_placeholder: str = "No available key mappings",
        long_help_separator: str = "  ",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

        self._short_help: BaseHelp = ShortHelp("short-help", toggle_key, short_help_separator, short_help_placeholder)
        self._long_help: BaseHelp = LongHelp("long-help", long_help_separator)

    def compose(self) -> ComposeResult:
        with ContentSwitcher(initial="short-help"):
            yield self._short_help
            yield self._long_help

    def toggle_view(self) -> None:
        switcher = self.query_one(ContentSwitcher)
        if switcher.current == "short-help" and self._short_help._can_switch():
            switcher.current = "long-help"
        else:
            switcher.current = "short-help"
