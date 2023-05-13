from __future__ import annotations

from rich.console import group
from rich.style import Style
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static

from examples._example_app import AppContainer, ExampleApp
from feathers.renderables import DividerWithLabel


class DividerBox(Static):
    def __init__(self, type: str, *, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(id=id, classes=classes)
        self.type = type

    def on_mount(self):
        if self.type == "simple":
            self.update(self._simple_dividers())

    @group()
    def _simple_dividers(self):
        end = "\n\n"
        yield DividerWithLabel("Namaste", end=end)
        yield DividerWithLabel("Hello", align="right", end=end)
        yield DividerWithLabel("Hola", align="center", end=end)
        yield DividerWithLabel("Bonjour", width=40, end=end)
        yield DividerWithLabel("Ciao", end=end, line_style=Style(color="grey37"))
        yield DividerWithLabel("Hallo", align="center", end=end, line_style=Style(color="green"))
        yield DividerWithLabel("你好", align="right", end=end, label_style=Style(color="magenta"))


class DividersContainer(AppContainer):
    def compose(self) -> ComposeResult:
        # we are not using grid as layers doesn't seem to work with it
        with Horizontal():
            yield DividerBox("simple", classes="box box-top-left")
        # with Horizontal():
        #     yield Container(
        #         Placeholder("This is a custom label for p1.", id="p1"),
        #     )
        #     yield Container(
        #         Placeholder("This is a custom label for p2.", id="p2"),
        #     )


class DividersViewApp(ExampleApp):
    CSS_PATH = "divider_with_label.css"

    header_title = "Dividers With Label"
    header_sub_title = "This demo showcase the DividerWithLabel renderable"

    def app_container(self) -> AppContainer:
        return DividersContainer()


if __name__ == "__main__":
    app = DividersViewApp()
    app.run()
