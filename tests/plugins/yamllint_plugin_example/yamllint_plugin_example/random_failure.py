# -*- coding: utf-8 -*-
# Copyright (C) 2020 Adrien Vergé
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


import random

from yamllint.linter import LintProblem


ID = 'random-failure'
TYPE = 'token'


def check(conf, token, prev, next, nextnext, context):
    if random.random() > 0.9:
        yield LintProblem(token.start_mark.line + 1,
                          token.start_mark.column + 1,
                          'random failure')
