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

   the following code snippet would **PASS**:
   ::

    platforms:
      - name: centos
        version: 8
      # - name: debian
      #   version: 10

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
from yamllint.rules.common import get_line_indent

ID = 'comments-indentation'
TYPE = 'comment'


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

def _enclosing_content_indents(buffer, pointer):
    """Return indents of content lines that enclose the line at *pointer*.

    Walking backward from that line, each non-empty, non-comment line whose
    indent is strictly smaller than the deepest indent seen so far is treated
    as an enclosing block (a parent sequence entry, mapping key, etc.).
    """
    line_start = buffer.rfind('\n', 0, pointer) + 1
    line_end = buffer.find('\n', line_start)
    if line_end == -1:
        line_end = len(buffer)
    line = buffer[line_start:line_end].rstrip('\r')
    stripped = line.lstrip(' ')
    indents = []
    min_seen = None
    if stripped and not stripped.startswith('#'):
        min_seen = len(line) - len(stripped)
        indents.append(min_seen)

    while line_start > 0:
        start = buffer.rfind('\n', 0, line_start - 1) + 1
        raw = buffer[start:line_start]
        if raw.endswith('\n'):
            raw = raw[:-1]
        if raw.endswith('\r'):
            raw = raw[:-1]
        line_start = start
        stripped = raw.lstrip(' ')
        if not stripped or stripped.startswith('#'):
            continue
        indent = len(raw) - len(stripped)
        if min_seen is None or indent < min_seen:
            indents.append(indent)
            min_seen = indent
            if min_seen == 0:
                break
    return indents


def check(conf, comment):
    # Only check block comments
    if (not isinstance(comment.token_before, yaml.StreamStartToken) and
            comment.token_before.end_mark.line + 1 == comment.line_no):
        return

    next_line_indent = comment.token_after.start_mark.column
    if isinstance(comment.token_after, yaml.StreamEndToken):
        next_line_indent = 0

    if isinstance(comment.token_before, yaml.StreamStartToken):
        prev_line_indent = 0
    else:
        prev_line_indent = get_line_indent(comment.token_before)

    # In the following case only the next line indent is valid:
    #     list:
    #         # comment
    #         - 1
    #         - 2
    prev_line_indent = max(prev_line_indent, next_line_indent)

    # If two indents are valid but a previous comment went back to normal
    # indent, for the next ones to do the same. In other words, avoid this:
    #     list:
    #         - 1
    #     # comment on valid indent (0)
    #         # comment on valid indent (4)
    #     other-list:
    #         - 2
    if (comment.comment_before is not None and
            not comment.comment_before.is_inline()):
        prev_line_indent = comment.comment_before.column_no - 1

    comment_indent = comment.column_no - 1
    valid = {prev_line_indent, next_line_indent}

    # When the next content is less indented, the previous line may sit
    # inside a nested mapping. Comments that close that nested block may
    # match an enclosing indent (the parent sequence entry, for example)
    # rather than only the nested line. See #384 and #141.
    if (comment_indent not in valid and
            comment.comment_before is None and
            not isinstance(comment.token_before, yaml.StreamStartToken) and
            next_line_indent < comment_indent < prev_line_indent):
        valid.update(_enclosing_content_indents(
            comment.token_before.start_mark.buffer,
            comment.token_before.start_mark.pointer))

    if comment_indent not in valid:
        yield LintProblem(comment.line_no, comment.column_no,
                          'comment not indented like content')
