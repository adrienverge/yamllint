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
        for problem in results[file]:
            max_level = max(max_level, PROBLEM_LEVELS[problem.level])
            if no_warn and (problem.level != 'error'):
                continue

            print(format_problem(problem, file))

    return max_level


def format_problem(problem, filename):
    return ('%(file)s:%(line)s:%(column)s: [%(level)s] %(message)s' %
            {'file': filename,
             'line': problem.line,
             'column': problem.column,
             'level': problem.level,
             'message': problem.message})
