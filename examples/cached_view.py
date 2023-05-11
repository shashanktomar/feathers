from __future__ import annotations

import random

from textual.app import App, ComposeResult

from feathers.widgets import CachedView


class CachedViewApp(App):
    CSS_PATH = "text_view.css"

    text = "Why do programmers prefer dark mode? Because light attracts bugs"

    def compose(self) -> ComposeResult:
        long = "\n".join([self.text[: random.randint(1, len(self.text))] for _ in range(10)])
        very_long = "\n".join([self.text[: random.randint(1, len(self.text))] for _ in range(60)])
        long_both_ways = (self.text * 4 + "\n") * 40
        yield CachedView(classes="box").write(self.text)
        yield CachedView(classes="box", enable_cursor=True).write(long)
        yield CachedView(classes="box").write(very_long)
        yield CachedView(classes="box", enable_cursor=True).write(long_both_ways)


if __name__ == "__main__":
    app = CachedViewApp()
    app.run()
