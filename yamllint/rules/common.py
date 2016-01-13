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


def max_spaces_after(nb, token, prev, next, description):
    if (next is not None and token.end_mark.line == next.start_mark.line and
            nb != - 1 and
            next.start_mark.pointer - token.end_mark.pointer > nb):
        return LintProblem(token.start_mark.line + 1, next.start_mark.column,
                           description)


def max_spaces_before(nb, token, prev, next, description):
    if (prev is not None and
            prev.end_mark.line == token.start_mark.line and
            nb != - 1 and
            prev.end_mark.pointer + nb < token.start_mark.pointer):
        return LintProblem(token.start_mark.line + 1, token.start_mark.column,
                           description)
