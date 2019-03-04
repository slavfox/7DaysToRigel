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
from abc import ABC
from typing import TYPE_CHECKING, Collection
from .helpers import Point
if TYPE_CHECKING:
    import tcod
    from .helpers import Pointlike


class Entity(ABC):
    __slots__ = [
        'location',

        'character',
        'color',

        'available_actions',
        'blocks_movement',
        'blocks_sight',
        'acts',

        'name',
        'description',
    ]

    def __init__(self,
                 # Fluff
                 name: str,
                 description: str,
                 location: Pointlike = None,
                 # Functionality
                 available_actions: Collection = (),
                 blocks_movement: bool = False,
                 blocks_sight: bool = False,
                 acts: bool = False,
                 # Visuals
                 character: int = None,
                 color: tcod.Color = None):
        self.location: Point = Point(location[0], location[1])

        self.name: str = name
        self.description: str = description

        self.available_actions: Collection = available_actions
        self.blocks_movement: bool = blocks_movement
        self.blocks_sight: bool = blocks_sight
        # Whether this entity acts on its own
        self.acts: bool = acts

        self.character: int = character
        self.color: tcod.Color = color


