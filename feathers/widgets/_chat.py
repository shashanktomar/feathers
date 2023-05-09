from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum

from rich.console import Console, ConsoleOptions, RenderResult
from rich.segment import Segment
from rich.style import Style
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget, events
from textual.widgets import TextLog


@dataclass
class Participant:
    name: str
    icon: str = ""
    color: str | None = None


@dataclass
class ChatEntry:
    message: str
    participant: Participant
    timestamp: float | None = None


class RenderableChatEntry:
    def __init__(self, renderer: ChatEntryRenderer, entry: ChatEntry) -> None:
        self._renderer = renderer
        self._entry = entry

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        return self._renderer.render(self._entry, console, options)


class ChatStyle(Enum):
    MINIMAL = "minimal"
    DETAILED = "detailed"


class ChatEntryRenderer:
    @abstractmethod
    def render(self, console: Console, entry: ChatEntry) -> RenderResult:
        pass


class MinimalChatRenderer(ChatEntryRenderer):
    def __init__(self) -> None:
        pass

    def render(self, entry: ChatEntry, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Text.assemble(
            (f"{entry.participant.name}: ", Style(color=entry.participant.color)),
            (entry.message, console.style),
            end="\n\n",
        )


class DetailedChatRenderer(ChatEntryRenderer):
    def render(self, entry: ChatEntry) -> str:
        return f"{entry.timestamp} - {entry.participant.name}: {entry.message}"


class Chat(Widget):
    RENDERER_MAPPING = {
        ChatStyle.MINIMAL: MinimalChatRenderer,
        ChatStyle.DETAILED: DetailedChatRenderer,
    }

    DEFAULT_CSS = """
    Chat {
        padding: 1;
    }
    """

    def __init__(
        self,
        chat_style: ChatStyle = ChatStyle.MINIMAL,
        highlight: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self._entries: list[ChatEntry] = []
        self.chat_style = chat_style

        self._chat_log = TextLog(wrap=True)
        self._entry_renderer = self.RENDERER_MAPPING[chat_style]()

    # called by textual
    def compose(self) -> ComposeResult:
        yield self._chat_log

    # called by textual
    def _on_resize(self, _: events.Resize) -> None:
        self._chat_log.refresh(layout=True)

    def add(self, entry: ChatEntry) -> None:
        self._entries.append(entry)
        # self._chat_log.write(RenderableChatEntry(self._entry_renderer, entry))
        text = Text.assemble(
            (f"{entry.participant.name}: ", Style(color=entry.participant.color)),
            (entry.message),
            end="\n\n",
        )
        self.log(text)
        self._chat_log.write(text)
        self.log(self.scrollable_content_region)
        self.log(self._chat_log.scrollable_content_region)
        self.log(self.content_size)
        self.log(self.content_region)

    def get_entries(self) -> list[ChatEntry]:
        return self._entries

    def clear(self) -> None:
        self._entries.clear()
        self._chat_log.clear()
        self.refresh()
