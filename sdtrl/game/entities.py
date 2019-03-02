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
from typing import Collection, TYPE_CHECKING
from engine import Entity, Color
if TYPE_CHECKING:
    from engine import Pointlike


class Creature(Entity):
    """
    A creature.
    """
    def __init__(self,
                 # Fluff
                 name: str,
                 description: str,
                 location: Pointlike,
                 # Functionality
                 available_actions: Collection = (),
                 blocks_movement: bool = True,
                 blocks_sight: bool = False,
                 acts: bool = True,
                 # Visuals
                 character: str = None,
                 color: Color = None):
        super().__init__(
            name=name,
            description=description,
            location=location,
            available_actions=available_actions,
            blocks_movement=blocks_movement,
            blocks_sight=blocks_sight,
            acts=acts,
            character=character,
            color=color
        )


class Player(Creature):
    def __init__(self, location: Pointlike):
        super().__init__(
            name="you",
            description="What a sexy beast you are.",
            location=location,
            # ToDo
            available_actions={'FIX ME!'},
            blocks_movement=False,
            blocks_sight=False,
            acts=True,
            character='@',
            color=Color(255, 255, 255)
        )
