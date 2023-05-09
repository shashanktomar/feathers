from __future__ import annotations

from collections.abc import Iterable

import rich.repr
from textual.strip import Strip


@rich.repr.auto
class Block:
    """Represents a 'block' (group of lines) of a Textual Widget.

    A Block is like an immutable list of Strips. The immutability allows for effective caching.

    Args:
        strips: An iterable of strips.
    """

    __slots__ = ["_strips", "_height"]

    def __init__(self, strips: Iterable[Strip]) -> None:
        self._strips = list(strips)
        self._height = None

    @property
    def height(self) -> int:
        """The height of block."""

        if self._height is None:
            self._height = len(list(self._strips))
        return self._height

    def __rich_repr__(self) -> rich.repr.Result:
        yield self._strips
