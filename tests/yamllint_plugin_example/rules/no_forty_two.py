#
# Copyright (C) 2020 Satoru SATOH
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
#
"""
Use this rule to forbid 42 in any values.

.. rubric:: Examples

#. With ``no-forty-two: {}``

   the following code snippet would **PASS**:
   ::

    the_answer: 1

   the following code snippet would **FAIL**:
   ::

    the_answer: 42
"""
import yaml

from yamllint.linter import LintProblem


ID = 'no-forty-two'
TYPE = 'token'


def check(conf, token, prev, next, nextnext, context):
    if (isinstance(token, yaml.ScalarToken) and
            isinstance(prev, yaml.ValueToken) and
            token.value == '42'):
        yield LintProblem(token.start_mark.line + 1,
                          token.start_mark.column + 1,
                          '42 is forbidden value')
