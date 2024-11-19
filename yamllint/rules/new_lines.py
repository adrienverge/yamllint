# Copyright (C) 2016 Adrien Vergé
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Use this rule to force the type of new line characters.

.. rubric:: Options

* Set ``type`` to ``unix`` to enforce UNIX-typed new line characters (``\\n``),
  set ``type`` to ``dos`` to enforce DOS-typed new line characters
  (``\\r\\n``), or set ``type`` to ``platform`` to infer the type from the
  system running yamllint (``\\n`` on POSIX / UNIX / Linux / Mac OS systems or
  ``\\r\\n`` on DOS / Windows systems).

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   new-lines:
     type: unix
"""

from os import linesep

from yamllint.linter import LintProblem

ID = 'new-lines'
TYPE = 'line'
CONF = {'type': ('unix', 'dos', 'platform')}
DEFAULT = {'type': 'unix'}


def check(conf, line):
    if conf['type'] == 'unix':
        newline_char = '\n'
    elif conf['type'] == 'platform':
        newline_char = linesep
    elif conf['type'] == 'dos':
        newline_char = '\r\n'

    if len(line.buffer) > line.end:
        if line.buffer[line.end:line.end + len(newline_char)] != newline_char:
            c = repr(newline_char).strip('\'')
            yield LintProblem(line.line_no, line.end - line.start + 1,
                              f'wrong new line character: expected {c}')
