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
from typing import TYPE_CHECKING, List, Callable, Tuple
from collections import OrderedDict

import tcod
from .helpers import Map, MemorizedCell, GameState

if TYPE_CHECKING:
    from .game import BaseGame
    from .helpers import CellContents
    from pathlib import Path
    from .helpers import SplashScreen


class UI:
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    LOGO_HEIGHT = 20

    TITLE: str = None
    FONT: Path = None
    FONT_SMALL: Path = None
    SPLASH_SCREEN: SplashScreen = None

    def __init__(self, game: BaseGame,
                 default_bg_color: tcod.Color = None,
                 default_fg_color: tcod.Color = None,
                 default_void_color: tcod.Color = None,
                 main_menu_options: OrderedDict[
                     str, Tuple[tcod.Color, Callable]
                 ] = None):

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

        if main_menu_options is None:
            self.main_menu_options = OrderedDict()
        else:
            self.main_menu_options = main_menu_options

        tcod.console_set_custom_font(
            fontFile=self.FONT.as_posix(),
            nb_char_horiz=16,
            nb_char_vertic=16
        )
        self.console: tcod.tcod.console.Console = None
        self.game: BaseGame = game
        self.memory: Map[List[MemorizedCell]] = None
        self.state = GameState.SPLASH
        self._end_credits = False
        self._selected_option_index = 0
        self._longest_option_length = max(
            len(opt) for opt in self.main_menu_options
        )
        self._main_menu_options_tuple = tuple(self.main_menu_options.keys())

    def init_root(self) -> tcod.tcod.console.Console:
        self.console = tcod.console_init_root(
            w=self.SCREEN_WIDTH,
            h=self.SCREEN_HEIGHT,
            title=self.TITLE,
            order='F'
        )
        return self.console

    def run(self):
        # self.console.print_box(
        #     0, self.SCREEN_HEIGHT-(credits_height + 1),
        #     self.SCREEN_WIDTH, credits_height,
        #     self.game.SPLASH_SCREEN.get_centered_credits(self.SCREEN_WIDTH),
        #     fg=tuple(self.game.SPLASH_SCREEN.credits_color),
        #     bg=(0, 0, 0)
        # )
        self.console.clear()
        while not tcod.console_is_window_closed():
            if self.state == GameState.SPLASH:
                self.draw_splash_screen()
                self.handle_splash_screen_keys()
            else:
                self.game.tick()
                self.draw_game()
        return

    def draw_game(self):
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
        ch: int = ord(' ')
        fg_color: tcod.Color = self.default_fg_color
        bg_color: tcod.Color = self.default_bg_color

        if self.game.is_visible((x, y)):
            cell: CellContents = self.game.world @ (x, y)
            if cell.tile:
                memorized_tile_name = cell.tile.name
                if cell.tile.fg_color:
                    fg_color = cell.tile.fg_color
                if cell.tile.bg_color:
                    bg_color = cell.tile.bg_color
                if cell.tile.character:
                    ch = cell.tile.character
            for entity in cell.entities:
                if entity.character:
                    # We don't set `ch` here, because we don't want to
                    # memorize entities.
                    self.console.ch[x, y] = entity.character
                    if entity.color:
                        fg_color = entity.color
                    break
            else:
                self.console.ch[x, y] = ch
            self.memory[y][x] = MemorizedCell(ch,
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

    def draw_splash_screen(self):
        # title_height = self.console.print_box(
        #     0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT,
        #     self.game.SPLASH_SCREEN.get_centered_title_art(self.SCREEN_WIDTH),
        #     fg=tuple(self.game.SPLASH_SCREEN.title_art_color)
        # )
        self.console.clear()

        self.draw_title()
        top_offset = self.LOGO_HEIGHT + 4
        # bottom_offset = self.draw_credits() + 1
        # remaining = self.SCREEN_HEIGHT - top_offset - bottom_offset - 1

        # Have to do it this way because libtcod has a weird interaction with
        # CP437 characters
        key_hint1 = f"Choose an option with {chr(18)}"
        key_hint2 = ", confirm with the Spacebar or Enter"
        xstart = (self.SCREEN_WIDTH - (len(key_hint1) + len(key_hint2))) // 2
        self.console.print(
            xstart, top_offset,
            key_hint1, fg=(112, 120, 128)
        )
        self.console.print(
            xstart + len(key_hint1), top_offset,
            key_hint2, fg=(112, 120, 128)
        )
        self.draw_main_menu_options(top_offset + 1)
        self.draw_credits()
        if not self._end_credits:
            self._end_credits = tcod.console_credits_render(
                self.SCREEN_WIDTH - 15, self.SCREEN_HEIGHT - 3, True
            )
        tcod.console_blit(self.console, 0, 0, self.SCREEN_WIDTH,
                          self.SCREEN_HEIGHT, self.console, 0, 0)
        tcod.console_flush()

    def draw_title(self):
        logo_width = int(
            (self.SPLASH_SCREEN.logo.width /
             self.SPLASH_SCREEN.logo.height) * self.LOGO_HEIGHT
        )
        self.SPLASH_SCREEN.logo.blit_rect(
            self.console,
            (self.SCREEN_WIDTH - logo_width) // 2, 1,
            logo_width, self.LOGO_HEIGHT,
            tcod.BKGND_SET
        )
        centered_title = self.SPLASH_SCREEN.get_centered_title(
            self.SCREEN_WIDTH
        )
        self.console.print_box(
            0, self.LOGO_HEIGHT + 2,
            self.SCREEN_WIDTH, centered_title.count('\n') + 1,
            centered_title,
            fg=tuple(self.SPLASH_SCREEN.title_color),
            bg=(0, 0, 0)
        )
        return self.LOGO_HEIGHT

    def draw_credits(self):
        for key, color in self.SPLASH_SCREEN.credits_format_colors.items():
            tcod.console_set_color_control(key, tuple(color), (0, 0, 0))
        credits_height = self.SPLASH_SCREEN.credits.count('\n') + 1
        self.console.print_box(
            0, self.SCREEN_HEIGHT - (credits_height + 1),
            self.SCREEN_WIDTH, credits_height,
            self.SPLASH_SCREEN.get_centered_credits(self.SCREEN_WIDTH),
            fg=tuple(self.SPLASH_SCREEN.credits_color),
            bg=(0, 0, 0)
        )
        return credits_height

    def draw_main_menu_options(self, yoffset):
        for i, option in enumerate(self.main_menu_options):
            fg = self.main_menu_options[option][0]
            bg = (0, 0, 0)
            if i == self._selected_option_index:
                fg, bg = bg, fg
            yoffset += 1
            self.console.print_frame(
                (self.SCREEN_WIDTH - self._longest_option_length - 2) // 2,
                yoffset,
                self._longest_option_length + 2,
                5
            )
            yoffset += 1
            self.console.print_box(
                (self.SCREEN_WIDTH - self._longest_option_length) // 2, yoffset,
                self._longest_option_length, 1,
                " " * self._longest_option_length,
                fg=fg, bg=bg
            )
            yoffset += 1
            self.console.print_box(
                (self.SCREEN_WIDTH - self._longest_option_length) // 2, yoffset,
                self._longest_option_length, 1,
                option.center(self._longest_option_length),
                fg=fg, bg=bg
            )
            yoffset += 1
            self.console.print_box(
                (self.SCREEN_WIDTH - self._longest_option_length) // 2, yoffset,
                self._longest_option_length, 1,
                " " * self._longest_option_length,
                fg=fg, bg=bg
            )
            yoffset += 2

    def handle_splash_screen_keys(self):
        key: tcod.Key = tcod.console_check_for_keypress()
        if not key:
            return
        if key.vk == tcod.KEY_DOWN:
            self._selected_option_index = min(
                len(self._main_menu_options_tuple) - 1,
                self._selected_option_index + 1
            )
        elif key.vk == tcod.KEY_UP:
            self._selected_option_index = max(
                0, self._selected_option_index - 1
            )
        elif key.vk in (tcod.KEY_SPACE, tcod.KEY_ENTER):
            self.main_menu_options[
                self._main_menu_options_tuple[self._selected_option_index]
            ][1]()

    def start_game(self):
        self.console.clear()
        self.game.start_game()
        self.memory = Map(
            self.game.world.map.width, self.game.world.map.height
        )
        self.state = GameState.GAME

    def prewarm_memory(self):
        ...

    @staticmethod
    def close_window():
        tcod.console_is_window_closed = lambda: True
