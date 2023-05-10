from __future__ import annotations

import random

from textual.app import App, ComposeResult

from feathers.widgets import TextView


class TextViewApp(App):
    CSS_PATH = "text_view.css"

    text = "Why do programmers prefer dark mode? Because light attracts bugs"

    def compose(self) -> ComposeResult:
        yield TextView(id="box-one", classes="box")
        yield TextView(id="box-two", classes="box")
        yield TextView(id="box-three", classes="box")
        yield TextView(id="box-four", classes="box")

    def on_mount(self) -> None:
        long = "\n".join([self.text[: random.randint(1, len(self.text))] for _ in range(10)])
        very_long = "\n".join([self.text[: random.randint(1, len(self.text))] for _ in range(60)])
        long_both_ways = (self.text * 4 + "\n") * 40

        self.query_one("#box-one").write(self.text)
        self.query_one("#box-two").write(long)
        self.query_one("#box-three").write(very_long)
        self.query_one("#box-four").write(long_both_ways)


if __name__ == "__main__":
    app = TextViewApp()
    app.run()
