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
    if isinstance(token, (yaml.StreamStartToken, yaml.StreamEndToken)):
        return

    # Check if first token in line
    if (not isinstance(prev, (yaml.StreamStartToken, yaml.DirectiveToken)) and
            token.start_mark.line == prev.end_mark.line):
        return

    if token.start_mark.column % conf['spaces'] != 0:
        yield LintProblem(
            token.end_mark.line + 1, token.start_mark.column + 1,
            'indentation is not a multiple of %d' % conf['spaces'])
        return

    if isinstance(prev, (yaml.StreamStartToken,
                         yaml.DirectiveToken,
                         yaml.DocumentStartToken,
                         yaml.DocumentEndToken)):
        indent = 0
    else:
        buffer = prev.end_mark.buffer
        start = buffer.rfind('\n', 0, prev.end_mark.pointer) + 1

        indent = 0
        while buffer[start + indent] == ' ':
            indent += 1

    if token.start_mark.column > indent:
        if not isinstance(prev, (yaml.BlockSequenceStartToken,
                                 yaml.BlockMappingStartToken,
                                 yaml.FlowSequenceStartToken,
                                 yaml.FlowMappingStartToken,
                                 yaml.KeyToken,
                                 yaml.ValueToken)):
            yield LintProblem(
                token.end_mark.line + 1, token.start_mark.column + 1,
                'unexpected indentation')

        elif token.start_mark.column != indent + conf['spaces']:
            yield LintProblem(
                token.end_mark.line + 1, token.start_mark.column + 1,
                'found indentation of %d instead of %d' %
                (token.start_mark.column, indent + conf['spaces']))
