from __future__ import annotations

from typing import cast

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.color import Color
from textual.widgets import Static

from feathers.widgets import Help, HelpEntry


class Box(Static, can_focus=True):
    BINDINGS = [
        Binding("k", "toggle_help_view", "move up", key_display="↑/k"),
        Binding("j", "toggle_help_view", "move down", key_display="↓/j"),
        Binding("c", "toggle_help_view", "some text", key_display="c"),
        Binding("d", "toggle_help_view", "delete", key_display="d"),
        Binding("e", "toggle_help_view", "explore", key_display="e"),
        Binding("f", "toggle_help_view", "find", key_display="f"),
        Binding("g", "toggle_help_view", "goto next", key_display="g"),
        Binding("h", "toggle_help_view", "hide", key_display="h"),
        Binding("i", "toggle_help_view", "Insert", key_display="i"),
        Binding("l", "toggle_help_view", "list", key_display="l"),
        Binding("n", "toggle_help_view", "new", key_display="n"),
        Binding("o", "toggle_help_view", "open", key_display="o"),
        Binding("p", "toggle_help_view", "preview", key_display="p"),
    ]

    def on_mount(self) -> None:
        self.update("Box")

    def short_help_keys(self) -> list[HelpEntry]:
        return [HelpEntry("↑/k", "move up"), HelpEntry("↓/j", "move down")]


class HelpDemo(App):
    CSS_PATH = "help_overlay.css"

    BINDINGS = [
        Binding("?", "toggle_help_view", "Toggle help", key_display="?"),
        Binding("p", "toggle_help_view", "preview", key_display="p"),
    ]

    def compose(self) -> ComposeResult:
        yield Box(classes="box")
        yield Box(classes="box")
        yield Help()

    def action_toggle_help_view(self) -> None:
        help = cast(Help, self.query_one("Help"))
        help.toggle_view()


if __name__ == "__main__":
    app = HelpDemo()
    app.run()
