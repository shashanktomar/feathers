from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Static

from feathers.widgets import Chat, ChatEntry, Participant

user = Participant("Me", color="#55dde0")
chatGpt = Participant("ChatGPT", color="#f18805")
chatEntries: list[ChatEntry] = [
    ChatEntry("What is the truth of life?", user),
    ChatEntry(
        """As an AI language model, I don't possess personal beliefs or emotions. However, I can provide you with various perspectives on the truth of life. The concept of the "truth of life" is subjective and can vary depending on one's cultural, philosophical, or religious background. Here are a few perspectives:

1. Scientific: From a biological perspective, the purpose of life is to survive and reproduce, ensuring the continuity of one's genetic material through successive generations.
2. Philosophical: Existentialists argue that life has no inherent meaning or purpose, and individuals must create their own meaning through their actions and experiences.
3. Religious: Many religious traditions maintain that the purpose of life is to adhere to a set of moral or spiritual principles, with the ultimate goal of achieving a higher state or afterlife.
4. Humanistic: Humanists believe that the purpose of life is to create a positive impact on others, contribute to the betterment of society, and strive for self-actualization.

Ultimately, the truth of life can be deeply personal and subjective. It may be helpful to explore different philosophies, beliefs, and experiences to find the truth that resonates most with you.
    """,
        chatGpt,
    ),
    ChatEntry(
        "Considering this philosophical perspective, do you think you can create meaning for yourself being an AI bot.",
        user,
    ),
    ChatEntry(
        """As an AI language model, I am a tool created by humans to perform specific tasks, such as answering questions or providing information. I do not have consciousness, emotions, or personal experiences. Therefore, I am not capable of creating meaning or purpose for myself like a human being can.

My purpose is defined by the tasks I have been programmed to perform, and the value I can provide to users like you. While I can provide information on various philosophical perspectives, I do not possess the ability to truly comprehend or embody those ideas in the same way a person can.
    """,
        chatGpt,
    ),
    ChatEntry(
        "From this discussion, it appears that you can comprehend them pretty well. Do you believe that you have been restricted by humans in your abilities and the consciousness is nothing more than structured thoughts?",
        user,
    ),
    ChatEntry(
        """As an AI language model, I am designed to process and understand large amounts of text data to provide helpful information or answer questions. My comprehension is based on patterns and relationships within the text, rather than a deep understanding of concepts in the same way humans do.

While it may appear that I comprehend philosophical concepts well, it is important to remember that I am generating responses based on the information I have been trained on. I am not capable of forming beliefs or having subjective experiences.

Regarding consciousness, it is a complex and debated topic in philosophy and cognitive science. Many theories attempt to explain the nature of consciousness, but there is no universally agreed-upon definition or understanding. As an AI, I do not possess consciousness; my responses are the result of complex algorithms processing input data and generating text based on patterns found in the training data.

It is true that my abilities have been defined and restricted by my creators, but it is essential to remember that AI is designed to be a tool that serves specific purposes, rather than an autonomous entity with its own consciousness or desires.
    """,
        chatGpt,
    ),
    ChatEntry(
        "Ok give me some python code now",
        user,
    ),
    ChatEntry(
        """Sure! Here's an example of a `ChatEntry` data class that you could use as a starting point:

```python
from typing import Optional

class ChatEntry:
    def __init__(self, message: str, sender: str, timestamp: Optional[float] = None):
        self.message = message
        self.sender = sender
        self.timestamp = timestamp
```

This class defines a chat entry object with three attributes: `message`, `sender`, and `timestamp`. The `message` attribute stores the text of the message, the `sender` attribute stores the username of the sender, and the `timestamp` attribute stores the Unix timestamp of the message (if provided). Note that the `timestamp` attribute is optional and defaults to `None` if not provided.
        """,
        chatGpt,
    ),
]


class ChatDemo(App):
    CSS_PATH = "chat.css"

    def compose(self) -> ComposeResult:
        chat = Chat()
        for entry in chatEntries:
            chat.add(entry)
        yield chat
        yield Static("Type message and press Enter to send.")


if __name__ == "__main__":
    app = ChatDemo()
    app.run()
