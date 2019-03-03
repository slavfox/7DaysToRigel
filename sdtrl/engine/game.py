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
from abc import ABC, abstractmethod
from typing import List, Iterable, Union, TYPE_CHECKING, Tuple, Type

import tcod
from .helpers import CellContents, Map

from .ui import UI

if TYPE_CHECKING:
    from .helpers import Pointlike
    from .entities import Entity
    from .tiles import Tile

__all__ = ['Map', 'BaseWorld', 'BaseGame']


class BaseWorld(ABC):
    def __init__(self, map_width, map_height):
        self.map: Map[List[Tile]] = Map(map_width, map_height)
        self.entities: List[Entity] = []

    @abstractmethod
    def get_visible_entities(self, from_: Pointlike) -> Iterable[Entity]:
        ...

    @abstractmethod
    def is_visible(self,
                   from_: Pointlike,
                   what: Union[Pointlike, Entity]) -> bool:
        """
        Check if an entity or a tile is visible from another given tile.
        :param from_: The starting point
        :param what: The target - either an Entity, or a Point
        """
        ...

    def __matmul__(
            self,
            coords: Tuple[int, int]
    ) -> CellContents:
        """
        Lets us do `world @ (x, y)` for prettiness.
        Returns the tile at given coordinates and entities there, in reverse
        draw order.
        """
        return CellContents(
            tile=self.map @ coords,
            entities=[ent for ent in self.entities if ent.location == coords]
        )


class BaseGame(ABC):
    """
    Base main class for the game. Your game should inherit from this.

    Remember to set the TITLE.
    """
    __slots__ = ['console', 'world', 'ui', 'player']
    UI_CLASS: Type[UI] = UI

    def __init__(self):
        self.world: BaseWorld = self.make_world()
        self.player: Entity = self.create_player_character()
        self.world.entities.append(self.player)
        self.ui: UI = self.UI_CLASS(self)
        self.console: tcod.tcod.console.Console = self.ui.init_root()

    @abstractmethod
    def make_world(self) -> BaseWorld:
        """
        Create and initialize the game world.
        """
        ...

    def tick(self, key: Union[tcod.Key, None] = None):
        self.handle_keypress(key)

    def get_visible_entities(self) -> Iterable[Entity]:
        """
        Get entities visible on the screen.
        """
        return self.world.get_visible_entities(
            self.player.location
        )

    def is_visible(self, what: Union[Pointlike, Entity]) -> bool:
        """
        Check if an entity or a tile is visible on the screen.
        :param what: The target - either an Entity, or a Point
        """
        return self.world.is_visible(self.player.location, what)

    @abstractmethod
    def create_player_character(self) -> Entity:
        ...

    @abstractmethod
    def handle_keypress(self, key: Union[tcod.Key, None]): ...
        # key: tcod.Key = tcod.console_check_for_keypress()

