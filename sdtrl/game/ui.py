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
from typing import TYPE_CHECKING, Tuple, Callable
from collections import OrderedDict

# noinspection PyPep8Naming
from engine import UI as BaseUI, SplashScreen, Color
from constants import ROOT_DIR, __version__, CREDITS, CREDITS_COLORS

if TYPE_CHECKING:
    from .game import BaseGame


class UI(BaseUI):
    TITLE = "7 Days to Rigel"
    FONT = ROOT_DIR/'assets'/'terminal.png'
    SPLASH_SCREEN = SplashScreen(
        title=f"v{__version__}. Developed for 7DRL'19.",
        # title_art=SPLASH_SCREEN,
        logo=ROOT_DIR / 'assets' / '7dtr_logo.png',
        credits=CREDITS,
        title_color=Color(129, 162, 190),
        credits_color=Color(197, 200, 198),
        credits_format_colors=CREDITS_COLORS
    )

    def __init__(self, game: BaseGame,
                 default_bg_color: Color = None,
                 default_fg_color: Color = None,
                 default_void_color: Color = None):
        super().__init__(
            game, default_bg_color, default_fg_color, default_void_color,
            main_menu_options=OrderedDict((
                (' Start Game ', (Color(204, 102, 102), self.start_game)),
                (' Options ', (Color(197, 200, 198), print)),
                (' Exit ', (Color(197, 200, 198), self.close_window)),
            ))
        )
