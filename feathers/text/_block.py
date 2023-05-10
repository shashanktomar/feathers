from __future__ import annotations

from collections.abc import Iterable, Iterator

import rich.repr
from textual.strip import Strip


@rich.repr.auto
class Block:
    """Represents a 'block' (group of lines) of a Textual Widget.

    A Block is like an immutable list of Strips. The immutability allows for effective caching.

    Args:
        strips: An iterable of strips.
    """

    __slots__ = ["_strips", "_max_len"]

    def __init__(self, strips: Iterable[Strip]) -> None:
        self._strips = list(strips)
        self._max_len: int | None = None

    @property
    def max_len(self) -> int:
        if self._max_len is None:
            if len(self) == 0:
                self._max_len = 0
            else:
                self._max_len = max(sum([segment.cell_length for segment in strip]) for strip in self._strips)
        return self._max_len

    def __len__(self) -> int:
        return len(list(self._strips))

    def __bool__(self) -> bool:
        return bool(self._strips)

    def __iter__(self) -> Iterator[Strip]:
        return iter(self._strips)

    def __getitem__(self, index) -> Strip:
        return self._strips[index]

    def __eq__(self, block: object) -> bool:
        return isinstance(block, Block) and (self._strips == block._strips)

    @classmethod
    def empty(cls) -> Block:
        return cls([])

    def add_strips(self, strips: list[Strip]) -> Block:
        """Merge the strips and return an new Block"""
        return Block(self._strips + strips)

    def extend(self, block: Block) -> Block:
        """Merge the strips and return an new Block"""
        return self.add_strips(block._strips)

    def __rich_repr__(self) -> rich.repr.Result:
        yield self._strips
