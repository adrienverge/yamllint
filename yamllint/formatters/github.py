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

from yamllint.linter import PROBLEM_LEVELS


def format_results(results, no_warn):
    max_level = 0

    for file in results:
        print('::group::%s' % file)

        for problem in results[file]:
            max_level = max(max_level, PROBLEM_LEVELS[problem.level])
            if no_warn and (problem.level != 'error'):
                continue

            print(format_problem(problem, file))

        print('::endgroup::')
        print('')

    return max_level


def format_problem(problem, filename):
    line = '::'
    line += problem.level
    line += ' file=' + filename + ','
    line += 'line=' + format(problem.line) + ','
    line += 'col=' + format(problem.column)
    line += '::'
    line += format(problem.line)
    line += ':'
    line += format(problem.column)
    line += ' '
    if problem.rule:
        line += '[' + problem.rule + '] '
    line += problem.desc
    return line
