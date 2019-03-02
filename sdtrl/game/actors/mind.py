# Adapted from Vibropyke.
# Relicensed GPL in accordance with Vibropyke's original MPL2.0 license.
#
#  Copyright (c) 2019 Slavfox
#
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
from dataclasses import dataclass
from typing import Set


@dataclass
class Fact:
    ...


@dataclass
class Mind:
    """
    An Actor's "brain". Stores knowledge and memory.
    """
    __slots__ = ['facts', 'memory']
    facts: Set
