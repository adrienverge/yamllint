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
Use this rule to force comments to be indented like content.

.. rubric:: Examples

#. With ``comments-indentation: {}``

   the following code snippet would **PASS**:
   ::

    # Fibonacci
    [0, 1, 1, 2, 3, 5]

   the following code snippet would **FAIL**:
   ::

      # Fibonacci
    [0, 1, 1, 2, 3, 5]

   the following code snippet would **PASS**:
   ::

    list:
        - 2
        - 3
        # - 4
        - 5

   the following code snippet would **FAIL**:
   ::

    list:
        - 2
        - 3
    #    - 4
        - 5

   the following code snippet would **PASS**:
   ::

    # This is the first object
    obj1:
      - item A
      # - item B
    # This is the second object
    obj2: []

   the following code snippet would **PASS**:
   ::

    # This sentence
    # is a block comment

   the following code snippet would **FAIL**:
   ::

    # This sentence
     # is a block comment
"""


import yaml

from yamllint.linter import LintProblem
from yamllint.rules.common import get_line_indent, get_comments_between_tokens


ID = 'comments-indentation'
TYPE = 'token'


# Case A:
#
#     prev: line:
#       # commented line
#       current: line
#
# Case B:
#
#       prev: line
#       # commented line 1
#     # commented line 2
#     current: line

def check(conf, token, prev, next, nextnext, context):
    if prev is None:
        return

    curr_line_indent = token.start_mark.column
    if isinstance(token, yaml.StreamEndToken):
        curr_line_indent = 0

    skip_first_line = True
    if isinstance(prev, yaml.StreamStartToken):
        skip_first_line = False
        prev_line_indent = 0
    else:
        prev_line_indent = get_line_indent(prev)

    if prev_line_indent <= curr_line_indent:
        prev_line_indent = -1  # disable it

    for comment in get_comments_between_tokens(
            prev, token, skip_first_line=skip_first_line):
        if comment.column - 1 == curr_line_indent:
            prev_line_indent = -1  # disable it
        elif comment.column - 1 != prev_line_indent:
            yield LintProblem(comment.line, comment.column,
                              'comment not indented like content')
