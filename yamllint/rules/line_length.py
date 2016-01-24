# -*- coding: utf-8 -*-
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
Use this rule to set a limit to lines length.

.. rubric:: Options

* ``max`` defines the maximal (inclusive) length of lines.

.. rubric:: Examples

#. With ``line-length: {max: 70}``

   the following code snippet would **PASS**:
   ::

    long sentence:
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
      eiusmod tempor incididunt ut labore et dolore magna aliqua.

   the following code snippet would **FAIL**:
   ::

    long sentence:
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua.
"""


from yamllint.linter import LintProblem


ID = 'line-length'
TYPE = 'line'
CONF = {'max': int}


def check(conf, line):
    if line.end - line.start > conf['max']:
        yield LintProblem(line.line_no, conf['max'] + 1,
                          'line too long (%d > %d characters)' %
                          (line.end - line.start, conf['max']))
