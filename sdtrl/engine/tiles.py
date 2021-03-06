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
from typing import Collection
import tcod


class Tile:
    __slots__ = [
        'character',
        'fg_color',
        'bg_color',

        'available_actions',
        'walkable',
        'blocks_sight',

        'name',
        'description',
        'type',
        'room'
    ]

    def __init__(self,
                 # Fluff
                 name: str,
                 description: str,
                 # Functionality
                 available_actions: Collection[str] = (),
                 walkable: bool = False,
                 blocks_sight: bool = False,
                 # Visuals
                 character: int = None,
                 fg_color: tcod.Color = None,
                 bg_color: tcod.Color = None,
                 room: str = None):
        # Functionality
        self.available_actions = available_actions
        self.walkable = walkable
        self.blocks_sight = blocks_sight

        # Fluff
        # These are instance variables to handle tiles of the same type that
        # might look or be functionally different (eg. segments of a table or
        # bloodstained/normal floors).
        self.name = name
        self.description = description
        self.room = room

        # Visuals
        self.character = character
        self.fg_color = fg_color
        self.bg_color = bg_color

    # noinspection PyProtectedMember
    def __copy__(self):
        return Tile(
            self.name,
            self.description,
            list(self.available_actions),
            self.walkable,
            self.blocks_sight,
            self.character,
            tcod.Color._new_from_cdata(self.fg_color),
            tcod.Color._new_from_cdata(self.bg_color)
        )

    def copy(self):
        return self.__copy__()

    def __str__(self):
        return chr(self.character) if self.character else ' '
