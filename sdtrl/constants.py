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
from pathlib import Path
from typing import NamedTuple

__all__ = ['version_info', '__version__', 'ROOT_DIR', 'SPLASH_SCREEN',
           'CREDITS']


class Version(NamedTuple):
    major: int
    minor: int
    patch: int


version_info: Version = Version(0, 1, 0)
__version__ = '.'.join(str(n) for n in version_info)
ROOT_DIR: Path = Path(__file__).resolve().parent

SPLASH_SCREEN = r'''

888888888888    88888888ba,
        ,8P'    88      `"8b
       d8"      88        `8b
     ,8P'       88         88 ,adPPYYba, 8b       d8 ,adPPYba,
    d8"         88         88 ""     `Y8 `8b     d8' I8[    ""
  ,8P'          88         8P ,adPPPPP88  `8b   d8'   `"Y8ba,
 d8"            88      .a8P  88,    ,88   `8b,d8'   aa    ]8I
8P'             88888888Y"'   `"8bbdP"Y8     Y88'    `"YbbdP"'
                                             d8'
                                            d8'

                      88888888ba  88                        88
  ,d                  88      "8b ""                        88
  88                  88      ,8P                           88
MM88MMM ,adPPYba,     88aaaaaa8P' 88  ,adPPYb,d8  ,adPPYba, 88
  88   a8"     "8a    88""""88'   88 a8"    `Y88 a8P_____88 88
  88   8b       d8    88    `8b   88 8b       88 8PP""""""" 88
  88,  "8a,   ,a8"    88     `8b  88 "8a,   ,d88 "8b,   ,aa 88
  "Y888 `"YbbdP"'     88      `8b 88  `"YbbdP"Y8  `"Ybbd8"' 88
                                      aa,    ,88
                                       "Y8bbdP"


'''
CREDITS = f"Licensed GPL. Copyright (c) Slavfox, 2019.\n" \
          f"@Slavfoxman   https://slavfox.io/" \
