from __future__ import annotations

import random
from typing import cast

from rich.style import Style
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding

from examples._example_app import AppContainer, ExampleApp
from feathers.widgets import CachedView, HelpEntry

TEXT = """Why did the text keep repeating itself? Because it couldn't resist its own words, so it said, "I'm going to repeat this joke!" And then it said it again, "I'm going to repeat this joke!" And just when you thought it was done, it said it one more time, "I'm going to repeat this joke!" It couldn't help it—it was trapped in an endless loop of its own humor!"""  # noqa: E501


class Container(AppContainer):
    entry_ids: list[int] = []

    def compose(self) -> ComposeResult:
        # we are not using grid as layers doesn't seem to work with it
        yield CachedView(id="box-one", classes="box")

    def _add_text(self, view: CachedView, id: int):
        text = Text(TEXT[: random.randint(1, len(TEXT))])
        view.add(text, str(id))

    def on_mount(self) -> None:
        box_one = cast(CachedView, self.query_one("#box-one"))

        box_text = Text(
            "Press `a` to add a new renderable, `r` to randomly remove on of the renderables and `u` to randomly update one of the renderables. The randomness is only for demo purpose, you can control what get removed and what get updated",  # noqa: E501
            style=Style(color="green"),
            end="\n\n",
        )
        box_one.add(box_text)

        for i in range(5):
            self._add_text(box_one, i)
            self.entry_ids.append(i)

    def on_add(self):
        box_one = cast(CachedView, self.query_one("#box-one"))

        box_one.remove("warning")
        id = len(self.entry_ids)
        self._add_text(box_one, id)
        self.entry_ids.append(id)

    def on_remove(self):
        box_one = cast(CachedView, self.query_one("#box-one"))

        if len(self.entry_ids) == 0:
            box_one.add(Text("Chill, nothing to remove mate!", style=Style(color="red")), id="warning")
        else:
            id_to_remove = random.choice(self.entry_ids)
            box_one.remove(str(id_to_remove))
            self.entry_ids.remove(id_to_remove)

    def on_update(self):
        pass


class CachedViewApp(ExampleApp):
    CSS_PATH = "cached_view_three.css"

    header_title = "CachedView Add, Remove and Update"
    header_sub_title = "This demo showcase the add, remove and update capabilities of a cached view"

    BINDINGS = [
        Binding("a", "add_text", "add text"),
        Binding("r", "remove_text", "remove text"),
        Binding("u", "update_text", "update text"),
    ]

    def app_container(self) -> AppContainer:
        return Container(id="app-container")

    def action_add_text(self):
        container = cast(Container, self.query_one("#app-container"))
        container.on_add()

    def action_remove_text(self):
        container = cast(Container, self.query_one("#app-container"))
        container.on_remove()

    def short_help_keys(self) -> list[HelpEntry]:
        return [
            HelpEntry("a", "add text"),
            HelpEntry("r", "remove text"),
            HelpEntry("u", "update text"),
        ]


if __name__ == "__main__":
    app = CachedViewApp()
    app.run()
