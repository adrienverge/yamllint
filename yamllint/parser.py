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

import yaml


class Line(object):
    def __init__(self, line_no, buffer, start, end):
        self.line_no = line_no
        self.start = start
        self.end = end
        self.buffer = buffer

    @property
    def content(self):
        return self.buffer[self.start:self.end]


class Token(object):
    def __init__(self, line_no, curr, prev, next, nextnext):
        self.line_no = line_no
        self.curr = curr
        self.prev = prev
        self.next = next
        self.nextnext = nextnext


def line_generator(buffer):
    line_no = 1
    cur = 0
    next = buffer.find('\n')
    while next != -1:
        yield Line(line_no, buffer, start=cur, end=next)
        cur = next + 1
        next = buffer.find('\n', cur)
        line_no += 1

    yield Line(line_no, buffer, start=cur, end=len(buffer))


def token_generator(buffer):
    yaml_loader = yaml.BaseLoader(buffer)

    try:
        prev = None
        curr = yaml_loader.get_token()
        while curr is not None:
            next = yaml_loader.get_token()
            nextnext = yaml_loader.peek_token()

            yield Token(curr.start_mark.line + 1, curr, prev, next, nextnext)

            prev = curr
            curr = next

    except yaml.scanner.ScannerError:
        pass


def token_or_line_generator(buffer):
    """Generator that mixes tokens and lines, ordering them by line number"""
    token_gen = token_generator(buffer)
    line_gen = line_generator(buffer)

    token = next(token_gen, None)
    line = next(line_gen, None)

    while token is not None or line is not None:
        if token is None or (line is not None and
                             token.line_no > line.line_no):
            yield line
            line = next(line_gen, None)
        else:
            yield token
            token = next(token_gen, None)
