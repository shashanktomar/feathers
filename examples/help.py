from __future__ import annotations

from typing import cast

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.color import Color
from textual.widgets import Static

from petals.widgets import Help, HelpEntry


class Bar(Static):
    pass


class ColorBars(Static, can_focus=True):
    BINDINGS = [
        Binding("r", "add_bar('red')", "Add Red"),
        Binding("g", "add_bar('green')", "add green"),
        Binding("b", "add_bar('blue')", "Add blue"),
    ]

    def compose(self):
        return []

    def action_add_bar(self, color: str) -> None:
        bar = Bar(color)
        bar.styles.background = Color.parse(color).with_alpha(0.5)
        self.mount(bar)
        self.call_after_refresh(self.screen.scroll_end, animate=False)

    def key_space(self) -> None:
        self.log("space pressed")

    # def short_help_keys(self) -> list[HelpEntry]:
    #     return [
    #         HelpEntry("r", "move up"),
    #         HelpEntry("g", "move down"),
    #         HelpEntry("b", "move down"),
    #     ]


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
    CSS_PATH = "help.css"

    BINDINGS = [
        Binding("?", "toggle_help_view", "Toggle help", key_display="?"),
    ]

    def compose(self) -> ComposeResult:
        yield Box(classes="column")
        yield ColorBars(classes="column")
        yield Help()

    def action_toggle_help_view(self) -> None:
        help = cast(Help, self.query_one("Help"))
        help.toggle_view()


if __name__ == "__main__":
    app = HelpDemo()
    app.run()
