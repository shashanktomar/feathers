import csv
import io

from rich.syntax import Syntax
from rich.table import Table
from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import cast

from examples._example_app import AppContainer, ExampleApp
from feathers.widgets import CachedView

CSV = """lane,swimmer,country,time
4,Joseph Schooling,Singapore,50.39
2,Michael Phelps,United States,51.14
5,Chad le Clos,South Africa,51.14
6,László Cseh,Hungary,51.14
3,Li Zhuhao,China,51.26
8,Mehdy Metella,France,51.58
7,Tom Shields,United States,51.73
1,Aleksandr Sadovnikov,Russia,51.84"""


CODE = '''\
def loop_first_last(values: Iterable[T]) -> Iterable[tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value\
'''


class Container(AppContainer):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield CachedView(id="box-one", highlight=True, markup=True, classes="box")
            yield CachedView(id="box-two", classes="box")

    async def on_mount(self) -> None:
        self._populate_box_one()

        box_two = cast(CachedView, self.query_one("#box-two"))
        box_two.border_title = "You can write a lot"
        for i in range(6000):
            box_two.add(f"{i} You can write a lot of content without loosing performance")

    def on_key(self, event: events.Key) -> None:
        """Write Key events to log."""
        view = cast(CachedView, self.query_one("#box-one"))
        view.add(event)

    def _populate_box_one(self) -> None:
        box_one = cast(CachedView, self.query_one("#box-one"))

        box_one.add(Syntax(CODE, "python", indent_guides=True, theme="github-dark"))

        rows = iter(csv.reader(io.StringIO(CSV)))
        table = Table(*next(rows))
        for row in rows:
            table.add_row(*row)

        box_one.add(table)
        box_one.border_title = "Really Rich Content"
        box_one.add("[green]Yow can write text or any Rich renderable to CachedView!")
        box_one.add("─" * 20)
        box_one.add("[bold magenta] ==> Press any key")
        box_one.add("─" * 20)


class CachedViewApp(ExampleApp):
    CSS_PATH = "cached_view_one.css"

    header_title = "CachedView Rendering"
    header_sub_title = "This demo showcase the rendering capabilities of a cached view"

    def app_container(self) -> AppContainer:
        return Container(id="container")

    def on_key(self, event: events.Key) -> None:
        """Write Key events to log."""
        view = cast(Container, self.query_one("#container"))
        view.on_key(event)


if __name__ == "__main__":
    app = CachedViewApp()
    app.run()
