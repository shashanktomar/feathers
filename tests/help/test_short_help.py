import pytest
from rich.text import Text
from textual.binding import Binding

from feathers.widgets import Help, HelpEntry

from .fixtures import HelpApp


@pytest.mark.asyncio
async def test_dock():
    """Should dock to bottom"""
    app = HelpApp()
    async with app.run_test():
        assert app.help.styles.dock == "bottom"


@pytest.mark.asyncio
async def test_short_help_is_default():
    """Should display short help by default"""
    app = HelpApp()
    async with app.run_test():
        help = app.query_one(Help)
        short_help = help.query_one("#short-help")
        long_help = help.query_one("#long-help")

        assert short_help.styles.display == "block"
        assert long_help.styles.display == "none"
        assert help.size.height == 1


@pytest.mark.asyncio
async def test_no_keys_for_app():
    """Should display placeholder text if no keys are available for the app"""
    app = HelpApp("Placeholder Text")
    async with app.run_test():
        help = app.query_one(Help)
        short_help = help.query_one("#short-help")

        assert app.focused is None
        assert short_help.renderable == Text("Placeholder Text")


@pytest.mark.asyncio
async def test_no_keys_for_widget():
    """Should display placeholder text if no keys are available for the widget"""
    app = HelpApp("Placeholder Text")
    async with app.run_test() as pilot:
        help = app.query_one(Help)
        short_help = help.query_one("#short-help")

        await pilot.press("tab")

        assert app.focused.id == "box-one"
        assert short_help.renderable == Text("Placeholder Text")


@pytest.mark.asyncio
async def test_toggle_key_for_app():
    """Should display toggle key, if app has keys and no widget is focused"""

    class AppWithKeys(HelpApp):
        BINDINGS = [
            Binding("k", "some_action", "move up", key_display="↑/k"),
        ]

    app = AppWithKeys()
    async with app.run_test():
        help = app.query_one(Help)
        short_help = help.query_one("#short-help")

        assert app.focused is None
        assert short_help.renderable.plain == "? toggle help"


@pytest.mark.asyncio
async def test_keys_for_widget():
    """Should display short keys, if focused widget has short keys"""

    app = HelpApp(box_one_short_keys=[HelpEntry("↑/k", "Move Up"), HelpEntry("↓/j", "move down")])
    async with app.run_test() as pilot:
        help = app.query_one(Help)
        short_help = help.query_one("#short-help")

        await pilot.press("tab")

        assert app.focused.id == "box-one"
        assert short_help.renderable.plain == "↑/k move up • ↓/j move down"
