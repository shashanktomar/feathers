from __future__ import annotations

from typing import cast

from rich.style import Style
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal

from examples._example_app import AppContainer, ExampleApp
from feathers.widgets import CachedView

TEXT_ONE = """Why did the chicken cross the road? To get to the other side! But then, why did the duck cross the road? To prove he wasn't chicken! And why did the turkey cross the road? To prove he wasn't a chicken either! But then, why did the cow cross the road? To get to the mooooooovies! And why did the sheep cross the road? To get to the ewe-nique boutique! And why did the horse cross the road? To get to the neigh-borhood bar! But why did the frog cross the road? To get to the croak-ery store! And why did the bee cross the road? To get to the honeycomb! And why did the snail cross the road? To get to the shell station!"""  # noqa: E501

# noqa: E501
TEXT_TWO = """Once upon a time, there was a chicken who wanted to prove that crossing the road was not just for mundane reasons. So, why did the chicken cross the road? To show off its impressive dance moves! With feathers flapping and a beak tapping, it wowed the onlookers on the other side. But then, why did the duck cross the road? To teach a traffic safety class for poultry! Quacking out instructions with authority, it made sure every feathered friend knew the importance of looking both ways.

Now, the chicken and the duck had started a trend, and soon enough, animals of all kinds joined in the road-crossing adventure. The turkey crossed the road, not to be outdone by its feathered counterparts, but to start a cooking show called 'Roadside Delights'—a feast on the move! With apron on, it sauntered across, sharing recipes for roadkill gourmet.

But wait, there's more! The cow, tired of the same old grazing routine, decided to cross the road to pursue its dream of becoming a famous stand-up comedian. Moo-ving gracefully, it entertained audiences on both sides with its witty jokes about life on the farm.

Meanwhile, the sheep, known for its impeccable fashion sense, crossed the road to reach the exclusive ewe-nique boutique, where it shopped for the latest trends in woolen wear. Donning stylish outfits, the sheep became a fashion icon, inspiring other animals to step up their fashion game.

Not to be left behind, the horse neighed with determination as it crossed the road, eager to reach the neigh-borhood bar for a refreshing drink. With a saddle as its favorite stool, it regaled fellow patrons with tales of wild horse races and daring adventures.

Even the frog couldn't resist the allure of the road, hopping across to get to the croak-ery store. It filled its cart with the finest assortment of lily pad plates and mosquito mugs, ensuring its amphibian friends would have a ribbiting dining experience.

Lastly, the bee buzzed its way across the road, embarking on a sweet mission to reach the honeycomb—nature's golden treasure. With its buzzing buddies, it constructed intricate hexagonal hives, producing honey that could rival the nectar of the gods.

And as if that wasn't enough, the snail, known for its slow and steady pace, crossed the road to get to the shell station. Carrying its home on its back, it refueled with slime-powered energy and continued its leisurely journey, undeterred by the fast-paced world around it.

So, you see, my friend, the road became a stage for adventures, dreams, and laughter. It was no longer a mere path from one place to another but a symbol of possibility and joy for all creatures, great and small. And that, my friend, is why they crossed the road!"""  # noqa: E501


class Container(AppContainer):
    text = "This is a single line of text, but you can still navigate it"

    style_msg = Style(color="green")
    merge_text = Text("\n\n")

    def compose(self) -> ComposeResult:
        # we are not using grid as layers doesn't seem to work with it
        with Horizontal():
            yield CachedView(id="box-one", classes="box-dim")
            yield CachedView(id="box-two", classes="box", enable_cursor=True)
            yield CachedView(id="box-three", classes="box", enable_cursor=True)
        with Horizontal():
            yield CachedView(id="box-four", classes="box", enable_cursor=True, auto_scroll=False)
            yield CachedView(id="box-five", classes="box", enable_cursor=True)
            yield CachedView(id="box-six", classes="box", enable_cursor=True)

    def on_mount(self) -> None:
        box_one = cast(CachedView, self.query_one("#box-one"))
        box_two = cast(CachedView, self.query_one("#box-two"))
        box_three = cast(CachedView, self.query_one("#box-three"))
        box_four = cast(CachedView, self.query_one("#box-four"))
        box_five = cast(CachedView, self.query_one("#box-five"))
        box_six = cast(CachedView, self.query_one("#box-six"))

        box_one.border_title = "Focus Disabled"
        box_one.add("This view is not focusable because cursor is disabled")

        box_two.border_title = "Single Line"
        box_two.add("I am a single line of text but you can still navigate me")

        box_text = Text("This is how you can navigate multi-line text", style=self.style_msg)
        box_three.border_title = "Multi Line"
        box_three.add(self.merge_text.join([box_text, Text(TEXT_ONE)]))

        box_text = Text("Here is a longer text. Try scrolling with navigation keys", style=self.style_msg)
        box_four.border_title = "Scrollable"
        box_four.add(self.merge_text.join([box_text, Text(TEXT_TWO)]))

        box_text = Text("This time we auto-scrolled to bottom. Try going up", style=self.style_msg)
        box_five.border_title = "Auto Scroll To Bottom"
        box_five.add(self.merge_text.join([Text(TEXT_TWO), box_text]))

        box_text = Text("This one scroll both ways", style=self.style_msg)
        box_six.border_title = "Scroll Both Ways"
        box_six.add(self.merge_text.join([Text(TEXT_TWO), box_text]), shrink=False)


class CachedViewApp(ExampleApp):
    CSS_PATH = "cached_view_two.css"

    header_title = "CachedView Navigation"
    header_sub_title = "This demo showcase the navigation capabilities of a cached view"

    def app_container(self) -> AppContainer:
        return Container()


if __name__ == "__main__":
    app = CachedViewApp()
    app.run()
