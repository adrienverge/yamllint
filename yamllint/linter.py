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

import codecs
import io
import re

import yaml

from yamllint import parser

PROBLEM_LEVELS = {
    0: None,
    1: 'warning',
    2: 'error',
    None: 0,
    'warning': 1,
    'error': 2,
}

DISABLE_RULE_PATTERN = re.compile(r'^# yamllint disable( rule:\S+)*\s*$')
ENABLE_RULE_PATTERN = re.compile(r'^# yamllint enable( rule:\S+)*\s*$')


class LintProblem:
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
            return '{} ({})'.format(self.desc, self.rule)
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


def get_cosmetic_problems(buffer, conf, filepath):
    rules = conf.enabled_rules(filepath)

    # Split token rules from line rules
    token_rules = [r for r in rules if r.TYPE == 'token']
    comment_rules = [r for r in rules if r.TYPE == 'comment']
    line_rules = [r for r in rules if r.TYPE == 'line']

    context = {}
    for rule in token_rules:
        context[rule.ID] = {}

    class DisableDirective:
        def __init__(self):
            self.rules = set()
            self.all_rules = {r.ID for r in rules}

        def process_comment(self, comment):
            comment = str(comment)

            if DISABLE_RULE_PATTERN.match(comment):
                items = comment[18:].rstrip().split(' ')
                rules = [item[5:] for item in items][1:]
                if len(rules) == 0:
                    self.rules = self.all_rules.copy()
                else:
                    for id in rules:
                        if id in self.all_rules:
                            self.rules.add(id)

            elif ENABLE_RULE_PATTERN.match(comment):
                items = comment[17:].rstrip().split(' ')
                rules = [item[5:] for item in items][1:]
                if len(rules) == 0:
                    self.rules.clear()
                else:
                    for id in rules:
                        self.rules.discard(id)

        def is_disabled_by_directive(self, problem):
            return problem.rule in self.rules

    class DisableLineDirective(DisableDirective):
        def process_comment(self, comment):
            comment = str(comment)

            if re.match(r'^# yamllint disable-line( rule:\S+)*\s*$', comment):
                items = comment[23:].rstrip().split(' ')
                rules = [item[5:] for item in items][1:]
                if len(rules) == 0:
                    self.rules = self.all_rules.copy()
                else:
                    for id in rules:
                        if id in self.all_rules:
                            self.rules.add(id)

    # Use a cache to store problems and flush it only when an end of line is
    # found. This allows the use of yamllint directive to disable some rules on
    # some lines.
    cache = []
    disabled = DisableDirective()
    disabled_for_line = DisableLineDirective()
    disabled_for_next_line = DisableLineDirective()

    for elem in parser.token_or_comment_or_line_generator(buffer):
        if isinstance(elem, parser.Token):
            for rule in token_rules:
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf,
                                          elem.curr, elem.prev, elem.next,
                                          elem.nextnext,
                                          context[rule.ID]):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    cache.append(problem)
        elif isinstance(elem, parser.Comment):
            for rule in comment_rules:
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf, elem):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    cache.append(problem)

            disabled.process_comment(elem)
            if elem.is_inline():
                disabled_for_line.process_comment(elem)
            else:
                disabled_for_next_line.process_comment(elem)
        elif isinstance(elem, parser.Line):
            for rule in line_rules:
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf, elem):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    cache.append(problem)

            # This is the last token/comment/line of this line, let's flush the
            # problems found (but filter them according to the directives)
            for problem in cache:
                if not (disabled_for_line.is_disabled_by_directive(problem) or
                        disabled.is_disabled_by_directive(problem)):
                    yield problem

            disabled_for_line = disabled_for_next_line
            disabled_for_next_line = DisableLineDirective()
            cache = []


def get_syntax_error(buffer):
    try:
        list(yaml.parse(buffer, Loader=yaml.BaseLoader))
    except yaml.error.MarkedYAMLError as e:
        problem = LintProblem(e.problem_mark.line + 1,
                              e.problem_mark.column + 1,
                              'syntax error: ' + e.problem + ' (syntax)')
        problem.level = 'error'
        return problem


def _read_yaml_unicode(f: io.IOBase) -> str:
    """Reads and decodes file as p.5.2. Character Encodings

       Parameters
       ----------
       f:
           For CLI - file open for reading in text mode
           (TextIOWrapper(BufferedReader(FileIO)))

           For API & tests - may be text or binary file object
           (StringIO, TextIOWrapper(BytesIO) or
           TextIOWrapper(BufferedReader(BytesIO)))
    """
    if not isinstance(f, io.TextIOWrapper):
        # StringIO already have unicode, don't need decode
        return (f.read(), False)

    b = f.buffer
    need = 4
    if not isinstance(b, io.BufferedReader):
        bs = bytes(b.getbuffer()[:need])  # BytesIO don't need peek()
    else:
        # Maximum of 4 raw.read()'s non-blocking file (or pipe)
        # are required for peek 4 bytes or achieve EOF
        lpbs = 0
        bs = b.peek(need)
        while len(bs) < need and len(bs) > lpbs:
            # len(bs) > lpbs <=> b.raw.read() returned some bytes, not EOF
            lpbs = len(bs)
            bs = b.peek(need)
        assert len(bs) >= need or not b.raw.read(1)

    if bs.startswith(codecs.BOM_UTF32_BE):
        f.reconfigure(encoding='utf-32be', errors='strict')
    elif bs.startswith(codecs.BOM_UTF32_LE):
        f.reconfigure(encoding='utf-32le', errors='strict')
    elif bs.startswith(codecs.BOM_UTF16_BE):
        f.reconfigure(encoding='utf-16be', errors='strict')
    elif bs.startswith(codecs.BOM_UTF16_LE):
        f.reconfigure(encoding='utf-16le', errors='strict')
    elif bs.startswith(codecs.BOM_UTF8):
        f.reconfigure(encoding='utf-8', errors='strict')
    elif bs.startswith(b'+/v8'):
        f.reconfigure(encoding='utf-7', errors='strict')
    else:
        if len(bs) >= 4 and bs[:3] == b'\x00\x00\x00' and bs[3]:
            f.reconfigure(encoding='utf-32be', errors='strict')
        elif len(bs) >= 4 and bs[0] and bs[1:4] == b'\x00\x00\x00':
            f.reconfigure(encoding='utf-32le', errors='strict')
        elif len(bs) >= 2 and bs[0] == 0 and bs[1]:
            f.reconfigure(encoding='utf-16be', errors='strict')
        elif len(bs) >= 2 and bs[0] and bs[1] == 0:
            f.reconfigure(encoding='utf-16le', errors='strict')
        else:
            f.reconfigure(encoding='utf-8', errors='strict')
        return (f.read(), False)
    initial_bom = f.read(1)
    assert initial_bom == '\uFEFF'
    return (f.read(), True)


def _run(input, conf, filepath):
    if isinstance(input, str):
        buffer, initial_bom = input, False
    else:
        try:
            buffer, initial_bom = _read_yaml_unicode(input)
        except UnicodeDecodeError as e:
            problem = LintProblem(0, 0, str(e), 'unicode-decode')
            problem.level = 'error'
            yield problem
            return

    first_line = next(parser.line_generator(buffer)).content
    if re.match(r'^#\s*yamllint disable-file\s*$', first_line):
        return

    if not initial_bom and first_line and not (first_line[0].isascii() and
       (first_line[0].isprintable() or first_line[0].isspace())):
        problem = LintProblem(1, 1,
                              "First Unicode character not ASCII without BOM",
                              'unicode-first-not-ascii')
        problem.level = 'warning'
        yield problem

    # If the document contains a syntax error, save it and yield it at the
    # right line
    syntax_error = get_syntax_error(buffer)

    for problem in get_cosmetic_problems(buffer, conf, filepath):
        # Insert the syntax error (if any) at the right place...
        if (syntax_error and syntax_error.line <= problem.line and
                syntax_error.column <= problem.column):
            yield syntax_error

            # Discard the problem since it is at the same place as the syntax
            # error and is probably redundant (and maybe it's just a 'warning',
            # in which case the script won't even exit with a failure status).
            syntax_error = None
            continue

        yield problem

    if syntax_error:
        yield syntax_error


def run(input, conf, filepath=None):
    """Lints a YAML source.

    Returns a generator of LintProblem objects.

    :param input: buffer, string or stream to read from
    :param conf: yamllint configuration object
    """
    if filepath is not None and conf.is_file_ignored(filepath):
        return ()

    if isinstance(input, str):
        return _run(input, conf, filepath)
    if isinstance(input, bytes):
        input = io.TextIOWrapper(io.BytesIO(input))
    if isinstance(input, io.IOBase):
        return _run(input, conf, filepath)
    raise TypeError('input should be a string or a stream')
