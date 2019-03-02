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
from typing import TYPE_CHECKING, List

import tcod
from .helpers import Map, MemorizedCell

if TYPE_CHECKING:
    from .game import BaseGame
    from .helpers import CellContents


class UI:
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    def __init__(self, game: BaseGame,
                 default_bg_color: tcod.Color = None,
                 default_fg_color: tcod.Color = None,
                 default_void_color: tcod.Color = None):

        if default_fg_color is None:
            self.default_fg_color = tcod.Color(255, 255, 255)
        else:
            self.default_fg_color = default_fg_color

        if default_bg_color is None:
            self.default_bg_color = tcod.Color(0, 0, 0)
        else:
            self.default_bg_color = default_bg_color

        if default_void_color is None:
            self.default_void_color = tcod.Color(0, 0, 0)
        else:
            self.default_void_color = default_void_color

        tcod.console_set_custom_font(
            fontFile=game.FONT.as_posix(),
            nb_char_horiz=16,
            nb_char_vertic=16
        )
        self.console: tcod.tcod.console.Console = None
        self.game: BaseGame = game
        self.memory: Map[List[MemorizedCell]] = Map(
            self.game.world.map.width, self.game.world.map.height
        )

    def init_root(self) -> tcod.tcod.console.Console:
        self.console = tcod.console_init_root(
            w=self.SCREEN_WIDTH,
            h=self.SCREEN_HEIGHT,
            title=self.game.TITLE,
            order='F'
        )
        return self.console

    def draw(self):
        for y in range(self.game.world.map.height):
            for x in range(self.game.world.map.width):
                self.draw_cell(x, y)
        tcod.console_blit(self.console, 0, 0, self.SCREEN_WIDTH,
                          self.SCREEN_HEIGHT, self.console, 0, 0)
        tcod.console_flush()

    def draw_cell(self, x: int, y: int) -> None:
        """
        Draw a cell from the world and memorize the contents.

        If there is nothing in the cell, we will try to remember what was there.
        """
        # Defaults, if there is nothing in the cell
        memorized_tile_name = None
        ch: str = ' '
        fg_color: tcod.Color = self.default_fg_color
        bg_color: tcod.Color = self.default_bg_color

        if self.game.is_visible((x, y)):
            cell: CellContents = self.game.world @ (x, y)
            if cell.tile:
                memorized_tile_name = cell.tile.name
                if cell.tile.bg_color:
                    bg_color = cell.tile.bg_color
                if cell.tile.character:
                    ch = ord(cell.tile.character)
            for entity in cell.entities:
                if entity.character:
                    # We don't set `ch` here, because we don't want to
                    # memorize entities.
                    self.console.ch[x, y] = ord(entity.character)
                    if entity.color:
                        fg_color = entity.color
                    break
            self.memory[x][y] = MemorizedCell(ch,
                                              fg_color * 0.5,
                                              bg_color * 0.5,
                                              memorized_tile_name)
        # If the cell isn't visible,
        else:
            memorized = self.memory @ (x, y)
            if memorized:
                ch, fg_color, bg_color = (
                    memorized.character, memorized.bg_color, memorized.fg_color
                )
                self.console.ch[x, y] = ch
        self.console.fg[x, y] = fg_color
        self.console.bg[x, y] = bg_color


