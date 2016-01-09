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


ID = 'colons'
TYPE = 'token'
CONF = {'max-spaces-before': int,
        'max-spaces-after': int}


def check(conf, token, prev, next):
    if isinstance(token, yaml.ValueToken):
        if (prev is not None and
                prev.end_mark.line == token.start_mark.line and
                conf['max-spaces-before'] != - 1 and
                (prev.end_mark.pointer + conf['max-spaces-before'] <
                 token.start_mark.pointer)):
            yield LintProblem(token.start_mark.line + 1,
                              token.start_mark.column,
                              'too many spaces before colon')

        if (next is not None and
                token.end_mark.line == next.start_mark.line and
                conf['max-spaces-after'] != - 1 and
                (next.start_mark.pointer - token.end_mark.pointer >
                 conf['max-spaces-after'])):
            yield LintProblem(token.start_mark.line + 1,
                              next.start_mark.column,
                              'too many spaces after colon')
