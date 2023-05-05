from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static

from feathers.widgets import Help, HelpEntry


class Box(Static, can_focus=True):
    DEFAULT_CSS = """
    Box {
        width: 1fr;
        height: 100%;
    }
    """

    def __init__(self, id, short_keys: list[HelpEntry] = []):
        super().__init__(id=id)
        self._short_keys = short_keys

    def short_help_keys(self) -> list[HelpEntry]:
        return self._short_keys


class HelpApp(App):
    DEFAULT_CSS = """
    TestApp {
        height: 100%;
    }
    """

    def __init__(self, placeholder_text="", box_one_short_keys: list[HelpEntry] = []):
        super().__init__()
        self.placeholder_text = placeholder_text
        self.help = Help(short_help_placeholder=self.placeholder_text)
        self._box_one_short_keys = box_one_short_keys

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Box(id="box-one", short_keys=self._box_one_short_keys)
            yield Box(id="box-two")
        yield self.help

    @classmethod
    def set_bindings(cls, bindings):
        cls.BINDINGS = bindings
