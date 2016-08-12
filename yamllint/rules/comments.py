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
Use this rule to control the position and formatting of comments.

.. rubric:: Options

* Use ``require-starting-space`` to require a space character right after the
  ``#``. Set to ``yes`` to enable, ``no`` to disable.
* ``min-spaces-from-content`` is used to visually separate inline comments from
  content. It defines the minimal required number of spaces between a comment
  and its preceding content.

.. rubric:: Examples

#. With ``comments: {require-starting-space: yes}``

   the following code snippet would **PASS**:
   ::

    # This sentence
    # is a block comment

   the following code snippet would **PASS**:
   ::

    ##############################
    ## This is some documentation

   the following code snippet would **FAIL**:
   ::

    #This sentence
    #is a block comment

#. With ``comments: {min-spaces-from-content: 2}``

   the following code snippet would **PASS**:
   ::

    x = 2 ^ 127 - 1  # Mersenne prime number

   the following code snippet would **FAIL**:
   ::

    x = 2 ^ 127 - 1 # Mersenne prime number
"""


from yamllint.linter import LintProblem


ID = 'comments'
TYPE = 'comment'
CONF = {'require-starting-space': bool,
        'min-spaces-from-content': int}


def check(conf, comment):
    if (conf['min-spaces-from-content'] != -1 and comment.is_inline() and
            comment.pointer - comment.token_before.end_mark.pointer <
            conf['min-spaces-from-content']):
        yield LintProblem(comment.line_no, comment.column_no,
                          'too few spaces before comment')

    if conf['require-starting-space']:
        text_start = comment.pointer + 1
        while (comment.buffer[text_start] == '#' and
               text_start < len(comment.buffer)):
            text_start += 1
        if (text_start < len(comment.buffer) and
                comment.buffer[text_start] not in (' ', '\n', '\0')):
            yield LintProblem(comment.line_no,
                              comment.column_no + text_start - comment.pointer,
                              'missing starting space in comment')
