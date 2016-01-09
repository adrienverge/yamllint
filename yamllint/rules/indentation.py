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

from yamllint.errors import LintProblem


ID = 'indentation'
TYPE = 'token'
CONF = {'spaces': int}


def check(conf, token, prev, next):
    if isinstance(token, yaml.StreamEndToken):
        return

    if (prev is None or isinstance(prev, yaml.StreamStartToken) or
            isinstance(prev, yaml.DirectiveToken) or
            isinstance(prev, yaml.DocumentStartToken)):
        if token.start_mark.column != 0:
            yield LintProblem(
                token.end_mark.line + 1, token.start_mark.column + 1,
                'found indentation of %d instead of %d' %
                (token.start_mark.column, 0))
        return

    if token.start_mark.line > prev.end_mark.line:
        buffer = prev.end_mark.buffer

        start = buffer.rfind('\n', 0, prev.end_mark.pointer) + 1
        prev_indent = 0

        # YAML recognizes two white space characters: space and tab.
        # http://yaml.org/spec/1.2/spec.html#id2775170
        while buffer[start + prev_indent] in ' \t':
            prev_indent += 1

        # Discard any leading '- '
        if (buffer[start + prev_indent:start + prev_indent + 2] == '- '):
            prev_indent += 2
            while buffer[start + prev_indent] in ' \t':
                prev_indent += 1

        if (token.start_mark.column > prev_indent and
                token.start_mark.column != prev_indent + conf['spaces']):
            yield LintProblem(
                token.end_mark.line + 1, token.start_mark.column + 1,
                'found indentation of %d instead of %d' %
                (token.start_mark.column, prev_indent + conf['spaces']))
