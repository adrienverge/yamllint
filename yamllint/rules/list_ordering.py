# Copyright (C) 2023 Johannes F. Knauf and Kevin Wojniak
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
Use this rule to enforce alphabetical ordering of items in lists. The sorting
order uses the Unicode code point number as a default. As a result, the
ordering is case-sensitive and not accent-friendly (see examples below).
This can be changed by setting the global ``locale`` option.  This allows one
to sort case and accents properly.

.. rubric:: Examples

#. With ``list-ordering: {}``

   the following code snippets would **PASS**:
   ::

    - key 1
    - key 2
    - key 3

    - [a, b, c]

    - T-shirt
    - T-shirts
    - t-shirt
    - t-shirts

    - hair
    - hais
    - haïr
    - haïssable

   the following code snippets would **FAIL**:
   ::

    - key 2
    - key 1

    - [b, a]

    - T-shirt
    - t-shirt
    - T-shirts
    - t-shirts

    - haïr
    - hais

#. With global option ``locale: "en_US.UTF-8"`` and rule ``list-ordering: {}``

   as opposed to before, the following code snippets would now **PASS**:
   ::

    - t-shirt
    - T-shirt
    - t-shirts
    - T-shirts

    - hair
    - haïr
    - hais
    - haïssable
"""

from locale import strcoll

import yaml

from yamllint.linter import LintProblem


ID = 'list-ordering'
TYPE = 'token'

MAP, SEQ = range(2)


class Parent:
    def __init__(self, type):
        self.type = type
        self.items = []


def check(conf, token, prev, next, nextnext, context):
    if 'stack' not in context:
        context['stack'] = []

    if isinstance(token, (yaml.BlockMappingStartToken,
                          yaml.FlowMappingStartToken)):
        context['stack'].append(Parent(MAP))
    elif isinstance(token, (yaml.BlockSequenceStartToken,
                            yaml.FlowSequenceStartToken)):
        context['stack'].append(Parent(SEQ))
    elif isinstance(token, (yaml.BlockEndToken,
                            yaml.FlowMappingEndToken,
                            yaml.FlowSequenceEndToken)):
        context['stack'].pop()
    elif isinstance(token, yaml.ScalarToken):
        if len(context['stack']) > 0 and context['stack'][-1].type == SEQ:
            if any(strcoll(token.value, item) < 0
                   for item in context['stack'][-1].items):
                yield LintProblem(
                    token.start_mark.line + 1, token.start_mark.column + 1,
                    'wrong list item order "%s"' % token.value)
            else:
                context['stack'][-1].items.append(token.value)
