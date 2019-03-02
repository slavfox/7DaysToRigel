#  Copyright (c) Slavfox, 2019.

# This file is part of 7 Days to Rigel.
#
# 7 Days to Rigel is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# 7 Days to Rigel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with 7 Days to Rigel.  If not, see <https://www.gnu.org/licenses/>.


# We pretty much reimplement namedtuple here to have the benefits of
# __slots__ but also define methods, have a Point be mutable and let it be
# unpacked.
from __future__ import annotations
from typing import NamedTuple, TYPE_CHECKING, List, Tuple, Optional, Union, \
    Sequence
from tcod import Color

if TYPE_CHECKING:
    from .tiles import Tile
    from .entities import Entity

__all__ = ['Color', 'Point', 'CellContents', 'Map', 'MemorizedCell',
           'Pointlike']


class Map(list):
    """
    A 2d array of tiles.
    """
    __slots__ = [
        'width', 'height'
    ]

    def __init__(self,
                 width: int,
                 height: int):
        super().__init__([[None] * height] * width)
        self.width = width
        self.height = height

    def __matmul__(self, coords: Tuple[int, int]) -> Tile:
        """
        Lets us do `map @ (x, y)` for prettiness
        """
        return self[coords[0]][coords[1]]


class Point(list):
    def __init__(self, x, y):
        super().__init__([x, y])

    @property
    def x(self) -> int:
        return self[0]

    @x.setter
    def x(self, val: int):
        self[0] = val

    @property
    def y(self) -> int:
        return self[1]

    @y.setter
    def y(self, val: int):
        self[1] = val

    def __iadd__(self, other):
        if len(other) != 2:
            raise TypeError("Can't add f{other} to a Point!")
        self[0] += other[0]
        self[1] += other[1]
        return self

    def __add__(self, other):
        if len(other) != 2:
            raise TypeError("Can't add f{other} to a Point!")
        return Point(self[0] + other[0], self[1] + other[1])

    def __isub__(self, other):
        if len(other) != 2:
            raise TypeError("Can't subtract f{other} from a Point!")
        self[0] += other[0]
        self[1] += other[1]
        return self

    def __sub__(self, other):
        if len(other) != 2:
            raise TypeError("Can't subtract f{other} from a Point!")
        return Point(self[0] + other[0], self[1] + other[1])

    def __eq__(self, other):
        return list(other) == list(self)


# Type alias for types compatible with Point, for ease of typing
Pointlike = Union[Point, Tuple[int, int], Sequence[int]]


class CellContents(NamedTuple):
    """
    Information about the contents of a tile in the world.
    """
    tile: Tile
    entities: List[Entity]


class MemorizedCell(NamedTuple):
    """
    A memorized cell, for drawing no-longer-visible tiles.
    """
    ch: str
    fg: Color
    bg: Color
    name: Optional[str]
