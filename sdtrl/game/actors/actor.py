# Adapted from Vibropyke.
# Relicensed GPL in accordance with Vibropyke's original MPL2.0 license.
#
#  Copyright (c) 2018, 2019 Slavfox
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


# Citations:
# - McCrae, R. and O. John 1992. An introduction to the five-factor
#   model and its applications. Journal of personality, 60(2):175–215.
# - Noonan, S. 2015. Side Quest Generation using Interactive Storytelling
#   for Open World Role Playing Games. Retrieved from https://scss.tcd.ie/publi-
#   cations/theses/diss/2015/TCD-SCSS-DISSERTATION-2015-050.pdf (Accessed
#   February 13. 2019)
@dataclass
class Personality:
    """
    Model of an Actor's personality, using the Five Factor Model.
    """
    __slots__ = ['openness', 'conscientiousness', 'extraversion',
                 'agreeableness', 'neuroticism']
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float


# Citations:
# - Bourgais, Mathieu, Taillandier, Patrick, Vercouter, Laurent and Adam, Carole
#   (2018) 'Emotion Modeling in Social Simulation: A Survey' Journal of
#   Artificial Societies and Social Simulation 21 (2) 5
#   <http://jasss.soc.surrey.ac.uk/21/2/5.html>. doi: 10.18564/jasss.3681
@dataclass
class Emotion:
    """
    Model of an Actor's emotional state.
    """
    __slots__ = ['arousal', 'valence', 'certainty']
    arousal: float
    valence: float
    certainty: float


class Actor:
    __slots__ = ['emotion', 'personality']

    def __init__(self, personality: Personality):
        self.emotion = Emotion(0,0,0)
        self.personality = personality

    def act(self): pass




