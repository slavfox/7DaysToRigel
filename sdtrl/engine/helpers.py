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
    Sequence, Dict
from dataclasses import dataclass
from enum import Enum
from textwrap import wrap

from tcod import Color, image_load

if TYPE_CHECKING:
    from tcod.image import Image
    from pathlib import Path
    from .tiles import Tile
    from .entities import Entity

__all__ = ['Color', 'Point', 'CellContents', 'Map', 'MemorizedCell',
           'Pointlike', 'GameState', 'SplashScreen']


@dataclass
class SplashScreen:
    title: str
    logo: Image
    credits: str
    credits_color: Color
    title_color: Color
    credits_format_colors: Dict[int, Color]

    # noinspection PyShadowingBuiltins
    def __init__(self, title: str, logo: Path, credits: str,
                 title_color: Color = None,
                 credits_color: Color = None,
                 credits_format_colors: Dict[int, Color] = None
                 ):
        if credits_format_colors is None:
            self.credits_format_colors = {}
        else:
            self.credits_format_colors = credits_format_colors
        self.title = title
        self.logo = image_load(logo.as_posix())
        self.credits = credits
        self._centered_title: str = None
        self._centered_credits: str = None
        self.title_color = title_color
        self.credits_color = credits_color

    def get_centered_credits(self, width: int) -> str:
        if self._centered_credits is None:
            self._centered_credits = "\n".join(
                line.center(width) for line in self.credits.split('\n')
            )
        return self._centered_credits

    def get_centered_title(self, width: int) -> str:
        if self._centered_title is None:
            self._centered_title = "\n".join(
                line.center(width) for line in wrap(self.title, width)
            )
        return self._centered_title

    # def get_centered_title_art(self, width: int) -> str:
    #     if self._centered_title_art is None:
    #         lines = self.title_art.split('\n')
    #         max_width = max(len(line) for line in lines)
    #         self._centered_title_art = "\n".join(
    #             line.ljust(max_width).center(width) for line in lines
    #         )
    #     return self._centered_title_art


class GameState(Enum):
    SPLASH = 0
    GAME = 1


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
        map_ = [] * height
        for y in range(height):
            map_.append([None] * width)
        super().__init__(map_)
        self.width = width
        self.height = height

    def __matmul__(self, coords: Tuple[int, int]) -> Tile:
        """
        Lets us do `map @ (x, y)` for prettiness
        """
        return self[coords[1]][coords[0]]

    def __repr__(self):
        return "\n".join(
            "".join(
                (chr(tile.character) if tile.character else ' ')
                if tile else '_'
                for tile in row)
            for row in self
        )

    def __str__(self):
        return self.__repr__()


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
    ch: int
    fg: Color
    bg: Color
    name: Optional[str]
