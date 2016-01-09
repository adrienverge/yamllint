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

from yamllint import config
from yamllint import parser


APP_NAME = 'yamllint'
APP_VERSION = '0.1.0'
APP_DESCRIPTION = 'Lint YAML files.'

__author__ = 'Adrien Vergé'
__copyright__ = 'Copyright 2016, Adrien Vergé'
__license__ = 'GPLv3'
__version__ = APP_VERSION


def _lint(buffer, conf):
    rules = config.get_enabled_rules(conf)

    # Split token rules from line rules
    token_rules = [r for r in rules if r.TYPE == 'token']
    line_rules = [r for r in rules if r.TYPE == 'line']

    # If the document contains a syntax error, save it and yield it at the
    # right line
    syntax_error = parser.get_syntax_error(buffer)

    for elem in parser.token_or_line_generator(buffer):
        if syntax_error and syntax_error.line <= elem.line_no:
            syntax_error.level = 'error'
            yield syntax_error
            syntax_error = None

        if isinstance(elem, parser.Token):
            for rule in token_rules:
                rule_conf = conf[rule.ID]
                for problem in rule.check(rule_conf,
                                          elem.curr, elem.prev, elem.next):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    yield problem
        elif isinstance(elem, parser.Line):
            for rule in line_rules:
                rule_conf = conf[rule.ID]
                for problem in rule.check(rule_conf, elem):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    yield problem


def lint(input, conf):
    """Lints a YAML source.

    Returns a generator of LintProblem objects.

    :param input: buffer, string or stream to read from
    :param conf: yamllint configuration object
    """
    if type(input) == str:
        return _lint(input, conf)
    elif hasattr(input, 'read'):  # Python 2's file or Python 3's io.IOBase
        # We need to have everything in memory to parse correctly
        content = input.read()
        return _lint(content, conf)
    else:
        raise TypeError('input should be a string or a stream')
