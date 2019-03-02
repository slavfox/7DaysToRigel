# 7 Days to Rigel

![GitHub top language](https://img.shields.io/github/languages/top/slavfox/7DaysToRigel.svg)
![GitHub](https://img.shields.io/github/license/slavfox/7DaysToRigel.svg)

**7 Days to Rigel** is a free and open-source roguelike
murder-mystery game written in seven days for [7DRL2019], and a 
proof-of-concept for a paper on procedural narrative generation and the use 
of promises in logic programming to circumvent the expression problem, to be
released at an as-of-yet undisclosed date in the future.

You can find my devlog at [slavfox.io]!

It's built on Python 3.7 and [python-libtcod], leveraging [kanren] and parts 
of code from (yet) unreleased personal projects Vibropyke and an early 
prototype of LorxuLang, for the logic programming parts. Those parts will later 
on, hopefully, be published as a full-featured Python logic programming 
framework.

## License

**7 Days to Rigel** is distributed under the [GNU General Public License], 
the full text of which can be found in the file [COPYING]. (The engine part of
the code might be released separately under a more permissive license in 
the future.)

Parts of the code (mainly [sdrl/game/actors]) were adapted from an unreleased 
personal research project on procedurally generated narrative, Vibropyke, and 
were originally licensed under the GPL-compatible 
[Mozilla Public License, v. 2.0.] As they are distributed here as a part of 
**7 Days to Rigel**, they are also licensed GPL, in accordance with the MPL's 
clause on [Distribution of a Larger Work (3.3)]. The source files contain a 
notice of that, where applicable.

The font used is provided by [python-libtcod] and is in the public domain.

[7DRL2019]: https://itch.io/jam/7drl-challenge-2019
[slavfox.io]: https://slavfox.io/
[python-libtcod]: https://github.com/libtcod/python-tcod
[kanren]: https://github.com/logpy/logpy
[sdrl/game/actors]: 
  https://github.com/slavfox/7DaysToRigel/blob/master/sdtrl/game/actors/actor.py
[GNU General Public License]: https://www.gnu.org/licenses/gpl.html
[COPYING]: https://github.com/slavfox/7DaysToRigel/blob/master/COPYING
[Mozilla Public License, v. 2.0.]: https://www.mozilla.org/en-US/MPL/2.0/
[Distribution of a Larger Work (3.3)]: 
  https://www.mozilla.org/en-US/MPL/2.0/#distribution-of-a-larger-work
