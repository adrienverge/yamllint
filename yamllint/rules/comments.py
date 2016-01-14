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

from yamllint.errors import LintProblem


ID = 'comments'
TYPE = 'token'
CONF = {'require-starting-space': bool,
        'min-spaces-from-content': int}


class Comment(object):
    def __init__(self, line, column, buffer, pointer):
        self.line = line
        self.column = column
        self.buffer = buffer
        self.pointer = pointer

    def __repr__(self):
        end = self.buffer.find('\n', self.pointer)
        if end == -1:
            end = self.buffer.find('\0', self.pointer)
        if end != -1:
            return self.buffer[self.pointer:end]
        return self.buffer[self.pointer:]

    def __eq__(self, other):
        return (self.line == other.line and
                self.column == other.column and
                str(self) == str(other))


def get_comments_until_next_token(token, next):
    if next is None:
        buf = token.end_mark.buffer[token.end_mark.pointer:]
    elif token.end_mark.line == next.start_mark.line:
        return
    else:
        buf = token.end_mark.buffer[token.end_mark.pointer:
                                    next.start_mark.pointer]

    line_no = token.end_mark.line + 1
    column_no = token.end_mark.column + 1
    pointer = token.end_mark.pointer

    for line in buf.split('\n'):
        pos = line.find('#')
        if pos != -1:
            yield Comment(line_no, column_no + pos,
                          token.end_mark.buffer, pointer + pos)

        pointer += len(line) + 1
        line_no += 1
        column_no = 1


def check(conf, token, prev, next):
    for comment in get_comments_until_next_token(token, next):
        if (conf['min-spaces-from-content'] != -1 and
                comment.line == token.end_mark.line + 1 and
                comment.pointer - token.end_mark.pointer <
                conf['min-spaces-from-content']):
            yield LintProblem(comment.line, comment.column,
                              'too few spaces before comment')

        if (conf['require-starting-space'] and
                comment.pointer + 1 < len(comment.buffer) and
                comment.buffer[comment.pointer + 1] != ' ' and
                comment.buffer[comment.pointer + 1] != '\n'):
            yield LintProblem(comment.line, comment.column + 1,
                              'missing starting space in comment')
