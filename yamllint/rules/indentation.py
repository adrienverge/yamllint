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
from yamllint.rules.common import is_explicit_key


ID = 'indentation'
TYPE = 'token'
CONF = {'spaces': int,
        'indent-sequences': (True, False, 'whatever')}

ROOT, MAP, B_SEQ, F_SEQ, KEY, VAL = range(6)


class Parent(object):
    def __init__(self, type, indent):
        self.type = type
        self.indent = indent
        self.explicit_key = False


def check_scalar_indentation(conf, token, context):
    if token.start_mark.line == token.end_mark.line:
        return

    if token.plain:
        expected_indent = token.start_mark.column
    elif token.style in ('"', "'"):
        expected_indent = token.start_mark.column + 1
    elif token.style in ('>', '|'):
        if context['stack'][-1].type == B_SEQ:
            # - >
            #     multi
            #     line
            expected_indent = token.start_mark.column + conf['spaces']
        elif context['stack'][-1].type == KEY:
            assert context['stack'][-1].explicit_key
            # - ? >
            #       multi-line
            #       key
            #   : >
            #       multi-line
            #       value
            expected_indent = token.start_mark.column + conf['spaces']
        elif context['stack'][-1].type == VAL:
            if token.start_mark.line + 1 > context['cur_line']:
                # - key:
                #     >
                #       multi
                #       line
                expected_indent = context['stack'][-1].indent + conf['spaces']
            elif context['stack'][-2].explicit_key:
                # - ? key
                #   : >
                #       multi-line
                #       value
                expected_indent = token.start_mark.column + conf['spaces']
            else:
                # - key: >
                #     multi
                #     line
                expected_indent = context['stack'][-2].indent + conf['spaces']
        else:
            expected_indent = context['stack'][-1].indent + conf['spaces']

    line_no = token.start_mark.line + 1

    line_start = token.start_mark.pointer
    while True:
        line_start = token.start_mark.buffer.find(
            '\n', line_start, token.end_mark.pointer - 1) + 1
        if line_start == 0:
            break
        line_no += 1

        indent = 0
        while token.start_mark.buffer[line_start + indent] == ' ':
            indent += 1
        if token.start_mark.buffer[line_start + indent] == '\n':
            continue

        if indent != expected_indent:
            yield LintProblem(line_no, indent + 1,
                              'wrong indentation: expected %d but found %d' %
                              (expected_indent, indent))


def check(conf, token, prev, next, context):
    if 'stack' not in context:
        context['stack'] = [Parent(ROOT, 0)]
        context['cur_line'] = -1

    # Step 1: Lint

    needs_lint = (
        not isinstance(token, (yaml.StreamStartToken, yaml.StreamEndToken)) and
        not isinstance(token, yaml.BlockEndToken) and
        not (isinstance(token, yaml.ScalarToken) and token.value == '') and
        token.start_mark.line + 1 > context['cur_line'])

    if needs_lint:
        found_indentation = token.start_mark.column
        expected = context['stack'][-1].indent

        if isinstance(token, (yaml.FlowMappingEndToken,
                              yaml.FlowSequenceEndToken)):
            expected = 0
        elif (context['stack'][-1].type == KEY and
                context['stack'][-1].explicit_key and
                not isinstance(token, yaml.ValueToken)):
            expected += conf['spaces']

        if found_indentation != expected:
            yield LintProblem(token.start_mark.line + 1, found_indentation + 1,
                              'wrong indentation: expected %d but found %d' %
                              (expected, found_indentation))

    if isinstance(token, yaml.ScalarToken):
        for problem in check_scalar_indentation(conf, token, context):
            yield problem

    # Step 2.a:

    if needs_lint:
        context['cur_line_indent'] = found_indentation
        context['cur_line'] = token.end_mark.line + 1

    # Step 2.b: Update state

    if isinstance(token, yaml.BlockMappingStartToken):
        assert isinstance(next, yaml.KeyToken)
        if next.start_mark.line == token.start_mark.line:
            #   - a: 1
            #     b: 2
            # or
            #   - ? a
            #     : 1
            indent = token.start_mark.column
        else:
            #   - ?
            #       a
            #     : 1
            indent = token.start_mark.column + conf['spaces']

        context['stack'].append(Parent(MAP, indent))

    elif isinstance(token, yaml.FlowMappingStartToken):
        if next.start_mark.line == token.start_mark.line:
            #   - {a: 1, b: 2}
            indent = next.start_mark.column
        else:
            #   - {
            #   a: 1, b: 2
            # }
            indent = context['cur_line_indent'] + conf['spaces']

        context['stack'].append(Parent(MAP, indent))

    elif isinstance(token, yaml.BlockSequenceStartToken):
        #   - - a
        #     - b
        assert next.start_mark.line == token.start_mark.line
        assert isinstance(next, yaml.BlockEntryToken)

        indent = token.start_mark.column

        context['stack'].append(Parent(B_SEQ, indent))

    elif isinstance(token, yaml.FlowSequenceStartToken):
        if next.start_mark.line == token.start_mark.line:
            #   - [a, b]
            indent = next.start_mark.column
        else:
            #   - [
            #   a, b
            # ]
            indent = context['cur_line_indent'] + conf['spaces']

        context['stack'].append(Parent(F_SEQ, indent))

    elif isinstance(token, (yaml.BlockEndToken,
                            yaml.FlowMappingEndToken,
                            yaml.FlowSequenceEndToken)):
        assert context['stack'][-1].type in (MAP, B_SEQ, F_SEQ)
        context['stack'].pop()

    elif isinstance(token, yaml.KeyToken):
        indent = context['stack'][-1].indent

        context['stack'].append(Parent(KEY, indent))

        context['stack'][-1].explicit_key = is_explicit_key(token)

    if context['stack'][-1].type == VAL:
        context['stack'].pop()
        assert context['stack'][-1].type == KEY
        context['stack'].pop()

    elif isinstance(token, yaml.ValueToken):
        assert context['stack'][-1].type == KEY

        # Discard empty values
        if isinstance(next, (yaml.BlockEndToken,
                             yaml.FlowMappingEndToken,
                             yaml.FlowSequenceEndToken,
                             yaml.KeyToken)):
            context['stack'].pop()
        else:
            if context['stack'][-1].explicit_key:
                #   ? k
                #   : value
                # or
                #   ? k
                #   :
                #     value
                indent = context['stack'][-1].indent + conf['spaces']
            elif next.start_mark.line == prev.start_mark.line:
                #   k: value
                indent = next.start_mark.column
            elif isinstance(next, (yaml.BlockSequenceStartToken,
                                   yaml.BlockEntryToken)):
                # NOTE: We add BlockEntryToken in the test above because
                # sometimes BlockSequenceStartToken are not issued. Try
                # yaml.scan()ning this:
                #     '- lib:\n'
                #     '  - var\n'
                if conf['indent-sequences'] is False:
                    indent = context['stack'][-1].indent
                elif conf['indent-sequences'] is True:
                    indent = context['stack'][-1].indent + conf['spaces']
                else:  # 'whatever'
                    if next.start_mark.column == context['stack'][-1].indent:
                        #   key:
                        #   - e1
                        #   - e2
                        indent = context['stack'][-1].indent
                    else:
                        #   key:
                        #     - e1
                        #     - e2
                        indent = context['stack'][-1].indent + conf['spaces']
            else:
                #   k:
                #     value
                indent = context['stack'][-1].indent + conf['spaces']

            context['stack'].append(Parent(VAL, indent))
