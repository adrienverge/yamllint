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


ID = 'new-line-at-end-of-file'
TYPE = 'line'


def check(conf, line):
    if line.end == len(line.buffer) and line.end > line.start:
        yield LintProblem(line.line_no, line.end - line.start + 1,
                          'no new line character at the end of file')
