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
from engine import BaseGame
from .world import World
from .entities import Player
from constants import ROOT_DIR


class SevenDaysToRigel(BaseGame):
    TITLE = "7 Days to Rigel"
    FONT = ROOT_DIR/'assets'/'terminal.png'

    def make_world(self) -> World:
        return World(80, 50)

    def create_player_character(self) -> Player:
        return Player(
            location=(self.world.map.width//2, self.world.map.height//2)
        )

    def handle_keypress(self):
        pass  # ToDo

