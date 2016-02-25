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

from yamllint import parser


class LintProblem(object):
    """Represents a linting problem found by yamllint."""
    def __init__(self, line, column, desc='<no description>', rule=None):
        #: Line on which the problem was found (starting at 1)
        self.line = line
        #: Column on which the problem was found (starting at 1)
        self.column = column
        #: Human-readable description of the problem
        self.desc = desc
        #: Identifier of the rule that detected the problem
        self.rule = rule
        self.level = None

    @property
    def message(self):
        if self.rule is not None:
            return '%s (%s)' % (self.desc, self.rule)
        return self.desc

    def __eq__(self, other):
        return (self.line == other.line and
                self.column == other.column and
                self.rule == other.rule)

    def __lt__(self, other):
        return (self.line < other.line or
                (self.line == other.line and self.column < other.column))

    def __repr__(self):
        return '%d:%d: %s' % (self.line, self.column, self.message)


def get_costemic_problems(buffer, conf):
    rules = conf.enabled_rules()

    # Split token rules from line rules
    token_rules = [r for r in rules if r.TYPE == 'token']
    line_rules = [r for r in rules if r.TYPE == 'line']

    context = {}
    for rule in token_rules:
        context[rule.ID] = {}

    for elem in parser.token_or_line_generator(buffer):
        if isinstance(elem, parser.Token):
            for rule in token_rules:
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf,
                                          elem.curr, elem.prev, elem.next,
                                          elem.nextnext,
                                          context[rule.ID]):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    yield problem
        elif isinstance(elem, parser.Line):
            for rule in line_rules:
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf, elem):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    yield problem


def get_syntax_error(buffer):
    try:
        list(yaml.parse(buffer, Loader=yaml.BaseLoader))
    except yaml.error.MarkedYAMLError as e:
        problem = LintProblem(e.problem_mark.line + 1,
                              e.problem_mark.column + 1,
                              'syntax error: ' + e.problem)
        problem.level = 'error'
        return problem


def _run(buffer, conf):
    # If the document contains a syntax error, save it and yield it at the
    # right line
    syntax_error = get_syntax_error(buffer)

    for problem in get_costemic_problems(buffer, conf):
        # Insert the syntax error (if any) at the right place...
        if (syntax_error and syntax_error.line <= problem.line and
                syntax_error.column <= problem.column):
            yield syntax_error

            # If there is already a yamllint error at the same place, discard
            # it as it is probably redundant (and maybe it's just a 'warning',
            # in which case the script won't even exit with a failure status).
            if (syntax_error.line == problem.line and
                    syntax_error.column == problem.column):
                syntax_error = None
                continue

            syntax_error = None

        yield problem

    if syntax_error:
        yield syntax_error


def run(input, conf):
    """Lints a YAML source.

    Returns a generator of LintProblem objects.

    :param input: buffer, string or stream to read from
    :param conf: yamllint configuration object
    """
    if type(input) in (type(b''), type(u'')):  # compat with Python 2 & 3
        return _run(input, conf)
    elif hasattr(input, 'read'):  # Python 2's file or Python 3's io.IOBase
        # We need to have everything in memory to parse correctly
        content = input.read()
        return _run(content, conf)
    else:
        raise TypeError('input should be a string or a stream')
