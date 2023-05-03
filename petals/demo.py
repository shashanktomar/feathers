from textual.app import App, ComposeResult

from petals.widgets import Help


class DemoApp(App):
    def compose(self) -> ComposeResult:
        yield Help()
