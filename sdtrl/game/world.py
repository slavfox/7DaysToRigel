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
from __future__ import annotations
from typing import TYPE_CHECKING, Iterable, Union, Collection, Tuple, \
    Callable, Sequence, List
import random
from dataclasses import dataclass

from engine import BaseWorld, Tile, Point
from tcod import Color

if TYPE_CHECKING:
    from engine import Pointlike, Entity

FLOOR_BG_COLOR = Color(29, 31, 33)
FLOOR_FG_COLOR = Color(40, 42, 46)
WALL_BG_COLOR = Color(55, 59, 65)
WALL_FG_COLOR = Color(112, 120, 128) # Color(40, 42, 46)
VIEWPORT_BG_COLOR = Color(0, 0, 0)
VIEWPORT_FG_COLOR = Color(112, 120, 128)


def floor_tile(room: str=None):
    return Tile(
        name="Floor",
        description="Empty floor.",
        bg_color=FLOOR_BG_COLOR,
        character=ord('.'),
        fg_color=FLOOR_FG_COLOR,
        walkable=True,
        room=room
    )

def wall_tile():
    return Tile(
        name="Wall",
        description="The ship's inner structure.",
        bg_color=WALL_BG_COLOR,
        character=ord('#'),
        fg_color=WALL_FG_COLOR,
        walkable=False,
        blocks_sight=True
    )

def viewport_tile():
    return Tile(
        name="Viewport",
        description="A window to the stars.",
        bg_color=VIEWPORT_BG_COLOR,
        character=9,  # ◘
        fg_color=VIEWPORT_FG_COLOR,
        walkable=False,
        blocks_sight=True
    )


def empty_square_room(w: int, h: int) -> Sequence[
    Sequence[Tuple[Tile, Sequence[Entity]]]
]:
    room: List[List[Tuple[Tile, List[Entity]]]] = []
    for rown in range(h):
        row: List[Tuple[Tile, List[Entity]]] = []
        for coln in range(w):
            row.append((floor_tile(), []))
        room.append(row)
    return room


@dataclass
class RoomDefinition:
    __slots__ = ['name', 'allowed_connections']
    name: str
    allowed_connections: Collection[str]
    min: int = 0
    max: int = float('inf')
    min_dimensions: Tuple[float, float] = (3, 3)
    max_dimensions: Tuple[float, float] = (float('inf'), float('inf'))
    gen: Callable[
        [int, int],
        Sequence[Sequence[Tuple[Tile, Sequence[Entity]]]]
    ] = empty_square_room
    required_connections: Collection[str] = ()

# 7 quarters
# bridge
# bar


class World(BaseWorld):
    def __init__(self, map_width, map_height):
        super().__init__(map_width, map_height)

    def get_visible_entities(self, from_: Pointlike) -> Iterable[Entity]:
        return []

    def is_visible(self,
                   from_: Pointlike, what: Union[Pointlike, Entity]) -> bool:
        return True  # ToDo

    def generate_map(self):
        self.generate_bridge()

    def generate_bridge(self):
        # Y width of bridge, including walls
        bridge_width = random.randint(5, 12)
        upper_right_corner_of_bridge = Point(
            self.map.width - 2,
            random.randint(1, self.map.height - bridge_width - 1)
        )
        bridge_length = random.randint(4, 8)
        for y in (upper_right_corner_of_bridge.y - 1,
                  upper_right_corner_of_bridge.y + bridge_width):
            for x in range(upper_right_corner_of_bridge.x - bridge_width - 1,
                           upper_right_corner_of_bridge.x + 1):
                print(y, x)
                self.map[y][x] = wall_tile()

        for y in range(upper_right_corner_of_bridge.y,
                       upper_right_corner_of_bridge.y + bridge_width):
            for x in range(upper_right_corner_of_bridge.x - bridge_width,
                           upper_right_corner_of_bridge.x):
                print(y, x)
                self.map[y][x] = floor_tile('Bridge')
        self.map[
            upper_right_corner_of_bridge.y
        ][
            upper_right_corner_of_bridge.x
        ] = wall_tile()
        self.map[
            upper_right_corner_of_bridge.y + bridge_width - 1
        ][
            upper_right_corner_of_bridge.x
        ] = wall_tile()
        for y in range(upper_right_corner_of_bridge.y + 1,
                       upper_right_corner_of_bridge.y + bridge_width - 1):
            self.map[y][upper_right_corner_of_bridge.x] = floor_tile()
        for y in range(upper_right_corner_of_bridge.y,
                       upper_right_corner_of_bridge.y + bridge_width):
            self.map[y][upper_right_corner_of_bridge.x + 1] = viewport_tile()
        print(self.map)
