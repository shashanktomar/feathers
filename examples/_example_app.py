from __future__ import annotations

from abc import abstractmethod
from typing import cast

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container

from examples._header import Header
from feathers.widgets import Help


class AppContainer(Container):
    def __init__(self, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(id=id, classes=classes)


class ExampleApp(App):
    DEFAULT_CSS = """
    Screen {
      layout: horizontal;
      layers: base overlay;
    }

    Header {
      layer: base;
    }

    AppContainer {
        width: 1fr;
        height: 1fr;
        margin-bottom: 1;
        layer: base;
     }

    Help {
      layer: overlay;
    }

    LongHelp {
      background: $background-lighten-1;
    }
    """

    BINDINGS = [
        Binding("?", "toggle_help_view", "Toggle help", key_display="?"),
    ]

    header_title: str = ""
    header_sub_title: str = ""

    @abstractmethod
    def app_container(self) -> AppContainer:
        pass

    def compose(self) -> ComposeResult:
        yield Header(self.header_title, self.header_sub_title)
        yield self.app_container()
        yield Help()

    def on_mount(self):
        self.log(self.query_one(Help))

    def action_toggle_help_view(self) -> None:
        help = cast(Help, self.query_one("Help"))
        help.toggle_help()
