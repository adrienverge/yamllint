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


def parsable_format(problem, filename):
    return ('%(file)s:%(line)s:%(column)s: [%(level)s] %(message)s' %
            {'file': filename,
             'line': problem.line,
             'column': problem.column,
             'level': problem.level,
             'message': problem.message})


def standard_format(problem, filename):
    line = '  \033[2m%d:%d\033[0m' % (problem.line, problem.column)
    line += max(20 - len(line), 0) * ' '
    if problem.level == 'warning':
        line += '\033[33m%s\033[0m' % problem.level
    else:
        line += '\033[31m%s\033[0m' % problem.level
    line += max(38 - len(line), 0) * ' '
    line += problem.desc
    if problem.rule:
        line += '  \033[2m(%s)\033[0m' % problem.rule
    return line
