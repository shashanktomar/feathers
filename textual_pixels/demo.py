from textual.app import App, ComposeResult

from textual_pixels.widgets import Help


class DemoApp(App):
    def compose(self) -> ComposeResult:
        yield Help()
