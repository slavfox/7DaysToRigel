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
from typing import TYPE_CHECKING, Iterable, Union
from engine import BaseWorld
if TYPE_CHECKING:
    from engine import Pointlike, Entity


class World(BaseWorld):

    def get_visible_entities(self, from_: Pointlike) -> Iterable[Entity]:
        return []

    def is_visible(self,
                   from_: Pointlike, what: Union[Pointlike, Entity]) -> bool:
        return True
