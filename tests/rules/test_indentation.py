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

from tests.common import RuleTestCase

from yamllint.parser import token_or_comment_generator, Comment
from yamllint.rules.indentation import check


class IndentationStackTestCase(RuleTestCase):
    # This test suite checks that the "indentation stack" built by the
    # indentation rule is valid. It is important, since everything else in the
    # rule relies on this stack.

    maxDiff = None

    def format_stack(self, stack):
        """Transform the stack at a given moment into a printable string like:

        B_MAP:0 KEY:0 VAL:5
        """
        return ' '.join(map(str, stack[1:]))

    def full_stack(self, source):
        conf = {'spaces': 2, 'indent-sequences': True,
                'check-multi-line-strings': False}
        context = {}
        output = ''
        for elem in [t for t in token_or_comment_generator(source)
                     if not isinstance(t, Comment)]:
            list(check(conf, elem.curr, elem.prev, elem.next, elem.nextnext,
                       context))

            token_type = (elem.curr.__class__.__name__
                          .replace('Token', '')
                          .replace('Block', 'B').replace('Flow', 'F')
                          .replace('Sequence', 'Seq')
                          .replace('Mapping', 'Map'))
            if token_type in ('StreamStart', 'StreamEnd'):
                continue
            output += '{:>9} {}\n'.format(token_type,
                                          self.format_stack(context['stack']))
        return output

    def test_simple_mapping(self):
        self.assertMultiLineEqual(
            self.full_stack('key: val\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:5\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('     key: val\n'),
            'BMapStart B_MAP:5\n'
            '      Key B_MAP:5 KEY:5\n'
            '   Scalar B_MAP:5 KEY:5\n'
            '    Value B_MAP:5 KEY:5 VAL:10\n'
            '   Scalar B_MAP:5\n'
            '     BEnd \n')

    def test_simple_sequence(self):
        self.assertMultiLineEqual(
            self.full_stack('- 1\n'
                            '- 2\n'
                            '- 3\n'),
            'BSeqStart B_SEQ:0\n'
            '   BEntry B_SEQ:0 B_ENT:2\n'
            '   Scalar B_SEQ:0\n'
            '   BEntry B_SEQ:0 B_ENT:2\n'
            '   Scalar B_SEQ:0\n'
            '   BEntry B_SEQ:0 B_ENT:2\n'
            '   Scalar B_SEQ:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('key:\n'
                            '  - 1\n'
                            '  - 2\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            'BSeqStart B_MAP:0 KEY:0 VAL:2 B_SEQ:2\n'
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:2 B_ENT:4\n'
            '   Scalar B_MAP:0 KEY:0 VAL:2 B_SEQ:2\n'
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:2 B_ENT:4\n'
            '   Scalar B_MAP:0 KEY:0 VAL:2 B_SEQ:2\n'
            '     BEnd B_MAP:0\n'
            '     BEnd \n')

    def test_non_indented_sequences(self):
        # There seems to be a bug in pyyaml: depending on the indentation, a
        # sequence does not produce the same tokens. More precisely, the
        # following YAML:
        #     usr:
        #       - lib
        # produces a BlockSequenceStartToken and a BlockEndToken around the
        # "lib" sequence, whereas the following:
        #     usr:
        #     - lib
        # does not (both two tokens are omitted).
        # So, yamllint must create fake 'B_SEQ'. This test makes sure it does.

        self.assertMultiLineEqual(
            self.full_stack('usr:\n'
                            '  - lib\n'
                            'var: cache\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            'BSeqStart B_MAP:0 KEY:0 VAL:2 B_SEQ:2\n'
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:2 B_ENT:4\n'
            '   Scalar B_MAP:0 KEY:0 VAL:2 B_SEQ:2\n'
            '     BEnd B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:5\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('usr:\n'
                            '- lib\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            # missing BSeqStart here
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            '   Scalar B_MAP:0\n'
            # missing BEnd here
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('usr:\n'
                            '- lib\n'
                            'var: cache\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            # missing BSeqStart here
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            '   Scalar B_MAP:0\n'
            # missing BEnd here
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:5\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('usr:\n'
                            '- []\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            # missing BSeqStart here
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            'FSeqStart B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 F_SEQ:3\n'
            '  FSeqEnd B_MAP:0\n'
            # missing BEnd here
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('usr:\n'
                            '- k:\n'
                            '    v\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            # missing BSeqStart here
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            'BMapStart B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_MAP:2\n'
            '      Key B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_MAP:2 KEY:2\n'
            '   Scalar B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_MAP:2 KEY:2\n'
            '    Value B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_MAP:2 KEY:2 VAL:4\n'  # noqa
            '   Scalar B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_MAP:2\n'
            '     BEnd B_MAP:0\n'
            # missing BEnd here
            '     BEnd \n')

    def test_flows(self):
        self.assertMultiLineEqual(
            self.full_stack('usr: [\n'
                            '  {k:\n'
                            '    v}\n'
                            '  ]\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:5\n'
            'FSeqStart B_MAP:0 KEY:0 VAL:5 F_SEQ:2\n'
            'FMapStart B_MAP:0 KEY:0 VAL:5 F_SEQ:2 F_MAP:3\n'
            '      Key B_MAP:0 KEY:0 VAL:5 F_SEQ:2 F_MAP:3 KEY:3\n'
            '   Scalar B_MAP:0 KEY:0 VAL:5 F_SEQ:2 F_MAP:3 KEY:3\n'
            '    Value B_MAP:0 KEY:0 VAL:5 F_SEQ:2 F_MAP:3 KEY:3 VAL:5\n'
            '   Scalar B_MAP:0 KEY:0 VAL:5 F_SEQ:2 F_MAP:3\n'
            '  FMapEnd B_MAP:0 KEY:0 VAL:5 F_SEQ:2\n'
            '  FSeqEnd B_MAP:0\n'
            '     BEnd \n')

    def test_anchors(self):
        self.assertMultiLineEqual(
            self.full_stack('key: &anchor value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:5\n'
            '   Anchor B_MAP:0 KEY:0 VAL:5\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('key: &anchor\n'
                            '  value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            '   Anchor B_MAP:0 KEY:0 VAL:2\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('- &anchor value\n'),
            'BSeqStart B_SEQ:0\n'
            '   BEntry B_SEQ:0 B_ENT:2\n'
            '   Anchor B_SEQ:0 B_ENT:2\n'
            '   Scalar B_SEQ:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('- &anchor\n'
                            '  value\n'),
            'BSeqStart B_SEQ:0\n'
            '   BEntry B_SEQ:0 B_ENT:2\n'
            '   Anchor B_SEQ:0 B_ENT:2\n'
            '   Scalar B_SEQ:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('- &anchor\n'
                            '  - 1\n'
                            '  - 2\n'),
            'BSeqStart B_SEQ:0\n'
            '   BEntry B_SEQ:0 B_ENT:2\n'
            '   Anchor B_SEQ:0 B_ENT:2\n'
            'BSeqStart B_SEQ:0 B_ENT:2 B_SEQ:2\n'
            '   BEntry B_SEQ:0 B_ENT:2 B_SEQ:2 B_ENT:4\n'
            '   Scalar B_SEQ:0 B_ENT:2 B_SEQ:2\n'
            '   BEntry B_SEQ:0 B_ENT:2 B_SEQ:2 B_ENT:4\n'
            '   Scalar B_SEQ:0 B_ENT:2 B_SEQ:2\n'
            '     BEnd B_SEQ:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('&anchor key:\n'
                            '  value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Anchor B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('pre:\n'
                            '  &anchor1 0\n'
                            '&anchor2 key:\n'
                            '  value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            '   Anchor B_MAP:0 KEY:0 VAL:2\n'
            '   Scalar B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Anchor B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('sequence: &anchor\n'
                            '- entry\n'
                            '- &anchor\n'
                            '  - nested\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            '   Anchor B_MAP:0 KEY:0 VAL:2\n'
            # missing BSeqStart here
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            '   Scalar B_MAP:0 KEY:0 VAL:2 B_SEQ:0\n'
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            '   Anchor B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            'BSeqStart B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_SEQ:2\n'
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_SEQ:2 B_ENT:4\n'
            '   Scalar B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_SEQ:2\n'
            '     BEnd B_MAP:0\n'
            # missing BEnd here
            '     BEnd \n')

    def test_tags(self):
        self.assertMultiLineEqual(
            self.full_stack('key: !!tag value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:5\n'
            '      Tag B_MAP:0 KEY:0 VAL:5\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('- !!map # Block collection\n'
                            '  foo : bar\n'),
            'BSeqStart B_SEQ:0\n'
            '   BEntry B_SEQ:0 B_ENT:2\n'
            '      Tag B_SEQ:0 B_ENT:2\n'
            'BMapStart B_SEQ:0 B_ENT:2 B_MAP:2\n'
            '      Key B_SEQ:0 B_ENT:2 B_MAP:2 KEY:2\n'
            '   Scalar B_SEQ:0 B_ENT:2 B_MAP:2 KEY:2\n'
            '    Value B_SEQ:0 B_ENT:2 B_MAP:2 KEY:2 VAL:8\n'
            '   Scalar B_SEQ:0 B_ENT:2 B_MAP:2\n'
            '     BEnd B_SEQ:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('- !!seq\n'
                            '  - nested item\n'),
            'BSeqStart B_SEQ:0\n'
            '   BEntry B_SEQ:0 B_ENT:2\n'
            '      Tag B_SEQ:0 B_ENT:2\n'
            'BSeqStart B_SEQ:0 B_ENT:2 B_SEQ:2\n'
            '   BEntry B_SEQ:0 B_ENT:2 B_SEQ:2 B_ENT:4\n'
            '   Scalar B_SEQ:0 B_ENT:2 B_SEQ:2\n'
            '     BEnd B_SEQ:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('sequence: !!seq\n'
                            '- entry\n'
                            '- !!seq\n'
                            '  - nested\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            '   Scalar B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:2\n'
            '      Tag B_MAP:0 KEY:0 VAL:2\n'
            # missing BSeqStart here
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            '   Scalar B_MAP:0 KEY:0 VAL:2 B_SEQ:0\n'
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            '      Tag B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2\n'
            'BSeqStart B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_SEQ:2\n'
            '   BEntry B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_SEQ:2 B_ENT:4\n'
            '   Scalar B_MAP:0 KEY:0 VAL:2 B_SEQ:0 B_ENT:2 B_SEQ:2\n'
            '     BEnd B_MAP:0\n'
            # missing BEnd here
            '     BEnd \n')

    def test_flows_imbrication(self):
        self.assertMultiLineEqual(
            self.full_stack('[[val]]\n'),
            'FSeqStart F_SEQ:1\n'
            'FSeqStart F_SEQ:1 F_SEQ:2\n'
            '   Scalar F_SEQ:1 F_SEQ:2\n'
            '  FSeqEnd F_SEQ:1\n'
            '  FSeqEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('[[val], [val2]]\n'),
            'FSeqStart F_SEQ:1\n'
            'FSeqStart F_SEQ:1 F_SEQ:2\n'
            '   Scalar F_SEQ:1 F_SEQ:2\n'
            '  FSeqEnd F_SEQ:1\n'
            '   FEntry F_SEQ:1\n'
            'FSeqStart F_SEQ:1 F_SEQ:9\n'
            '   Scalar F_SEQ:1 F_SEQ:9\n'
            '  FSeqEnd F_SEQ:1\n'
            '  FSeqEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('{{key}}\n'),
            'FMapStart F_MAP:1\n'
            'FMapStart F_MAP:1 F_MAP:2\n'
            '   Scalar F_MAP:1 F_MAP:2\n'
            '  FMapEnd F_MAP:1\n'
            '  FMapEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('[key]: value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            'FSeqStart B_MAP:0 KEY:0 F_SEQ:1\n'
            '   Scalar B_MAP:0 KEY:0 F_SEQ:1\n'
            '  FSeqEnd B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:7\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('[[key]]: value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            'FSeqStart B_MAP:0 KEY:0 F_SEQ:1\n'
            'FSeqStart B_MAP:0 KEY:0 F_SEQ:1 F_SEQ:2\n'
            '   Scalar B_MAP:0 KEY:0 F_SEQ:1 F_SEQ:2\n'
            '  FSeqEnd B_MAP:0 KEY:0 F_SEQ:1\n'
            '  FSeqEnd B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:9\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('{key}: value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            'FMapStart B_MAP:0 KEY:0 F_MAP:1\n'
            '   Scalar B_MAP:0 KEY:0 F_MAP:1\n'
            '  FMapEnd B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:7\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('{key: value}: value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            'FMapStart B_MAP:0 KEY:0 F_MAP:1\n'
            '      Key B_MAP:0 KEY:0 F_MAP:1 KEY:1\n'
            '   Scalar B_MAP:0 KEY:0 F_MAP:1 KEY:1\n'
            '    Value B_MAP:0 KEY:0 F_MAP:1 KEY:1 VAL:6\n'
            '   Scalar B_MAP:0 KEY:0 F_MAP:1\n'
            '  FMapEnd B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:14\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('{{key}}: value\n'),
            'BMapStart B_MAP:0\n'
            '      Key B_MAP:0 KEY:0\n'
            'FMapStart B_MAP:0 KEY:0 F_MAP:1\n'
            'FMapStart B_MAP:0 KEY:0 F_MAP:1 F_MAP:2\n'
            '   Scalar B_MAP:0 KEY:0 F_MAP:1 F_MAP:2\n'
            '  FMapEnd B_MAP:0 KEY:0 F_MAP:1\n'
            '  FMapEnd B_MAP:0 KEY:0\n'
            '    Value B_MAP:0 KEY:0 VAL:9\n'
            '   Scalar B_MAP:0\n'
            '     BEnd \n')
        self.assertMultiLineEqual(
            self.full_stack('{{key}: val, {key2}: {val2}}\n'),
            'FMapStart F_MAP:1\n'
            '      Key F_MAP:1 KEY:1\n'
            'FMapStart F_MAP:1 KEY:1 F_MAP:2\n'
            '   Scalar F_MAP:1 KEY:1 F_MAP:2\n'
            '  FMapEnd F_MAP:1 KEY:1\n'
            '    Value F_MAP:1 KEY:1 VAL:8\n'
            '   Scalar F_MAP:1\n'
            '   FEntry F_MAP:1\n'
            '      Key F_MAP:1 KEY:1\n'
            'FMapStart F_MAP:1 KEY:1 F_MAP:14\n'
            '   Scalar F_MAP:1 KEY:1 F_MAP:14\n'
            '  FMapEnd F_MAP:1 KEY:1\n'
            '    Value F_MAP:1 KEY:1 VAL:21\n'
            'FMapStart F_MAP:1 KEY:1 VAL:21 F_MAP:22\n'
            '   Scalar F_MAP:1 KEY:1 VAL:21 F_MAP:22\n'
            '  FMapEnd F_MAP:1\n'
            '  FMapEnd \n')

        self.assertMultiLineEqual(
            self.full_stack('{[{{[val]}}, [{[key]: val2}]]}\n'),
            'FMapStart F_MAP:1\n'
            'FSeqStart F_MAP:1 F_SEQ:2\n'
            'FMapStart F_MAP:1 F_SEQ:2 F_MAP:3\n'
            'FMapStart F_MAP:1 F_SEQ:2 F_MAP:3 F_MAP:4\n'
            'FSeqStart F_MAP:1 F_SEQ:2 F_MAP:3 F_MAP:4 F_SEQ:5\n'
            '   Scalar F_MAP:1 F_SEQ:2 F_MAP:3 F_MAP:4 F_SEQ:5\n'
            '  FSeqEnd F_MAP:1 F_SEQ:2 F_MAP:3 F_MAP:4\n'
            '  FMapEnd F_MAP:1 F_SEQ:2 F_MAP:3\n'
            '  FMapEnd F_MAP:1 F_SEQ:2\n'
            '   FEntry F_MAP:1 F_SEQ:2\n'
            'FSeqStart F_MAP:1 F_SEQ:2 F_SEQ:14\n'
            'FMapStart F_MAP:1 F_SEQ:2 F_SEQ:14 F_MAP:15\n'
            '      Key F_MAP:1 F_SEQ:2 F_SEQ:14 F_MAP:15 KEY:15\n'
            'FSeqStart F_MAP:1 F_SEQ:2 F_SEQ:14 F_MAP:15 KEY:15 F_SEQ:16\n'
            '   Scalar F_MAP:1 F_SEQ:2 F_SEQ:14 F_MAP:15 KEY:15 F_SEQ:16\n'
            '  FSeqEnd F_MAP:1 F_SEQ:2 F_SEQ:14 F_MAP:15 KEY:15\n'
            '    Value F_MAP:1 F_SEQ:2 F_SEQ:14 F_MAP:15 KEY:15 VAL:22\n'
            '   Scalar F_MAP:1 F_SEQ:2 F_SEQ:14 F_MAP:15\n'
            '  FMapEnd F_MAP:1 F_SEQ:2 F_SEQ:14\n'
            '  FSeqEnd F_MAP:1 F_SEQ:2\n'
            '  FSeqEnd F_MAP:1\n'
            '  FMapEnd \n')


class IndentationTestCase(RuleTestCase):
    rule_id = 'indentation'

    def test_disabled(self):
        conf = 'indentation: disable'
        self.check('---\n'
                   'object:\n'
                   '   k1: v1\n'
                   'obj2:\n'
                   ' k2:\n'
                   '     - 8\n'
                   ' k3:\n'
                   '           val\n'
                   '...\n', conf)
        self.check('---\n'
                   '  o:\n'
                   '    k1: v1\n'
                   '  p:\n'
                   '   k3:\n'
                   '       val\n'
                   '...\n', conf)
        self.check('---\n'
                   '     - o:\n'
                   '         k1: v1\n'
                   '     - p: kdjf\n'
                   '     - q:\n'
                   '        k3:\n'
                   '              - val\n'
                   '...\n', conf)

    def test_one_space(self):
        conf = 'indentation: {spaces: 1, indent-sequences: false}'
        self.check('---\n'
                   'object:\n'
                   ' k1:\n'
                   ' - a\n'
                   ' - b\n'
                   ' k2: v2\n'
                   ' k3:\n'
                   ' - name: Unix\n'
                   '   date: 1969\n'
                   ' - name: Linux\n'
                   '   date: 1991\n'
                   '...\n', conf)
        conf = 'indentation: {spaces: 1, indent-sequences: true}'
        self.check('---\n'
                   'object:\n'
                   ' k1:\n'
                   '  - a\n'
                   '  - b\n'
                   ' k2: v2\n'
                   ' k3:\n'
                   '  - name: Unix\n'
                   '    date: 1969\n'
                   '  - name: Linux\n'
                   '    date: 1991\n'
                   '...\n', conf)

    def test_two_spaces(self):
        conf = 'indentation: {spaces: 2, indent-sequences: false}'
        self.check('---\n'
                   'object:\n'
                   '  k1:\n'
                   '  - a\n'
                   '  - b\n'
                   '  k2: v2\n'
                   '  k3:\n'
                   '  - name: Unix\n'
                   '    date: 1969\n'
                   '  - name: Linux\n'
                   '    date: 1991\n'
                   '  k4:\n'
                   '  -\n'
                   '  k5: v3\n'
                   '...\n', conf)
        conf = 'indentation: {spaces: 2, indent-sequences: true}'
        self.check('---\n'
                   'object:\n'
                   '  k1:\n'
                   '    - a\n'
                   '    - b\n'
                   '  k2: v2\n'
                   '  k3:\n'
                   '    - name: Unix\n'
                   '      date: 1969\n'
                   '    - name: Linux\n'
                   '      date: 1991\n'
                   '...\n', conf)

    def test_three_spaces(self):
        conf = 'indentation: {spaces: 3, indent-sequences: false}'
        self.check('---\n'
                   'object:\n'
                   '   k1:\n'
                   '   - a\n'
                   '   - b\n'
                   '   k2: v2\n'
                   '   k3:\n'
                   '   - name: Unix\n'
                   '     date: 1969\n'
                   '   - name: Linux\n'
                   '     date: 1991\n'
                   '...\n', conf)
        conf = 'indentation: {spaces: 3, indent-sequences: true}'
        self.check('---\n'
                   'object:\n'
                   '   k1:\n'
                   '      - a\n'
                   '      - b\n'
                   '   k2: v2\n'
                   '   k3:\n'
                   '      - name: Unix\n'
                   '        date: 1969\n'
                   '      - name: Linux\n'
                   '        date: 1991\n'
                   '...\n', conf)

    def test_consistent_spaces(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              indent-sequences: whatever}\n'
                'document-start: disable\n')
        self.check('---\n'
                   'object:\n'
                   ' k1:\n'
                   '  - a\n'
                   '  - b\n'
                   ' k2: v2\n'
                   ' k3:\n'
                   '  - name: Unix\n'
                   '    date: 1969\n'
                   '  - name: Linux\n'
                   '    date: 1991\n'
                   '...\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  k1:\n'
                   '  - a\n'
                   '  - b\n'
                   '  k2: v2\n'
                   '  k3:\n'
                   '  - name: Unix\n'
                   '    date: 1969\n'
                   '  - name: Linux\n'
                   '    date: 1991\n'
                   '...\n', conf)
        self.check('---\n'
                   'object:\n'
                   '   k1:\n'
                   '      - a\n'
                   '      - b\n'
                   '   k2: v2\n'
                   '   k3:\n'
                   '      - name: Unix\n'
                   '        date: 1969\n'
                   '      - name: Linux\n'
                   '        date: 1991\n'
                   '...\n', conf)
        self.check('first is not indented:\n'
                   '  value is indented\n', conf)
        self.check('first is not indented:\n'
                   '     value:\n'
                   '          is indented\n', conf)
        self.check('- first is already indented:\n'
                   '    value is indented too\n', conf)
        self.check('- first is already indented:\n'
                   '       value:\n'
                   '            is indented too\n', conf)
        self.check('- first is already indented:\n'
                   '       value:\n'
                   '             is indented too\n', conf, problem=(3, 14))
        self.check('---\n'
                   'list one:\n'
                   '  - 1\n'
                   '  - 2\n'
                   '  - 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf, problem=(7, 5))
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '  - a\n'
                   '  - b\n'
                   '  - c\n', conf)
        self.check('---\n'
                   'list one:\n'
                   ' - 1\n'
                   ' - 2\n'
                   ' - 3\n'
                   'list two:\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf)

    def test_consistent_spaces_and_indent_sequences(self):
        conf = 'indentation: {spaces: consistent, indent-sequences: true}'
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf, problem1=(3, 1))
        self.check('---\n'
                   'list one:\n'
                   '  - 1\n'
                   '  - 2\n'
                   '  - 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf, problem1=(7, 5))
        self.check('---\n'
                   'list one:\n'
                   '  - 1\n'
                   '  - 2\n'
                   '  - 3\n'
                   'list two:\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf, problem1=(7, 1))

        conf = 'indentation: {spaces: consistent, indent-sequences: false}'
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf, problem1=(7, 5))
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '  - a\n'
                   '  - b\n'
                   '  - c\n', conf, problem1=(7, 3))
        self.check('---\n'
                   'list one:\n'
                   '  - 1\n'
                   '  - 2\n'
                   '  - 3\n'
                   'list two:\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf, problem1=(3, 3))

        conf = ('indentation: {spaces: consistent,\n'
                '              indent-sequences: consistent}')
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf, problem1=(7, 5))
        self.check('---\n'
                   'list one:\n'
                   '    - 1\n'
                   '    - 2\n'
                   '    - 3\n'
                   'list two:\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf, problem1=(7, 1))
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf)
        self.check('---\n'
                   'list one:\n'
                   '  - 1\n'
                   '  - 2\n'
                   '  - 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf, problem1=(7, 5))

        conf = 'indentation: {spaces: consistent, indent-sequences: whatever}'
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf)
        self.check('---\n'
                   'list one:\n'
                   '    - 1\n'
                   '    - 2\n'
                   '    - 3\n'
                   'list two:\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf)
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf)
        self.check('---\n'
                   'list one:\n'
                   '  - 1\n'
                   '  - 2\n'
                   '  - 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf, problem1=(7, 5))

    def test_indent_sequences_whatever(self):
        conf = 'indentation: {spaces: 4, indent-sequences: whatever}'
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf)
        self.check('---\n'
                   'list one:\n'
                   '  - 1\n'
                   '  - 2\n'
                   '  - 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf, problem=(3, 3))
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '  - a\n'
                   '  - b\n'
                   '  - c\n', conf, problem=(7, 3))
        self.check('---\n'
                   'list:\n'
                   '    - 1\n'
                   '    - 2\n'
                   '    - 3\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf, problem=(6, 1, 'syntax'))

    def test_indent_sequences_consistent(self):
        conf = 'indentation: {spaces: 4, indent-sequences: consistent}'
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list:\n'
                   '    two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf)
        self.check('---\n'
                   'list one:\n'
                   '    - 1\n'
                   '    - 2\n'
                   '    - 3\n'
                   'list:\n'
                   '    two:\n'
                   '        - a\n'
                   '        - b\n'
                   '        - c\n', conf)
        self.check('---\n'
                   'list one:\n'
                   '- 1\n'
                   '- 2\n'
                   '- 3\n'
                   'list two:\n'
                   '    - a\n'
                   '    - b\n'
                   '    - c\n', conf, problem=(7, 5))
        self.check('---\n'
                   'list one:\n'
                   '    - 1\n'
                   '    - 2\n'
                   '    - 3\n'
                   'list two:\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf, problem=(7, 1))
        self.check('---\n'
                   'list one:\n'
                   ' - 1\n'
                   ' - 2\n'
                   ' - 3\n'
                   'list two:\n'
                   '- a\n'
                   '- b\n'
                   '- c\n', conf, problem1=(3, 2), problem2=(7, 1))

    def test_direct_flows(self):
        # flow: [ ...
        # ]
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   'a: {x: 1,\n'
                   '    y,\n'
                   '    z: 1}\n', conf)
        self.check('---\n'
                   'a: {x: 1,\n'
                   '   y,\n'
                   '    z: 1}\n', conf, problem=(3, 4))
        self.check('---\n'
                   'a: {x: 1,\n'
                   '     y,\n'
                   '    z: 1}\n', conf, problem=(3, 6))
        self.check('---\n'
                   'a: {x: 1,\n'
                   '  y, z: 1}\n', conf, problem=(3, 3))
        self.check('---\n'
                   'a: {x: 1,\n'
                   '    y, z: 1\n'
                   '}\n', conf)
        self.check('---\n'
                   'a: {x: 1,\n'
                   '  y, z: 1\n'
                   '}\n', conf, problem=(3, 3))
        self.check('---\n'
                   'a: [x,\n'
                   '    y,\n'
                   '    z]\n', conf)
        self.check('---\n'
                   'a: [x,\n'
                   '   y,\n'
                   '    z]\n', conf, problem=(3, 4))
        self.check('---\n'
                   'a: [x,\n'
                   '     y,\n'
                   '    z]\n', conf, problem=(3, 6))
        self.check('---\n'
                   'a: [x,\n'
                   '  y, z]\n', conf, problem=(3, 3))
        self.check('---\n'
                   'a: [x,\n'
                   '    y, z\n'
                   ']\n', conf)
        self.check('---\n'
                   'a: [x,\n'
                   '  y, z\n'
                   ']\n', conf, problem=(3, 3))

    def test_broken_flows(self):
        # flow: [
        #   ...
        # ]
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   'a: {\n'
                   '  x: 1,\n'
                   '  y, z: 1\n'
                   '}\n', conf)
        self.check('---\n'
                   'a: {\n'
                   '  x: 1,\n'
                   '  y, z: 1}\n', conf)
        self.check('---\n'
                   'a: {\n'
                   '   x: 1,\n'
                   '  y, z: 1\n'
                   '}\n', conf, problem=(4, 3))
        self.check('---\n'
                   'a: {\n'
                   '  x: 1,\n'
                   '  y, z: 1\n'
                   '  }\n', conf, problem=(5, 3))
        self.check('---\n'
                   'a: [\n'
                   '  x,\n'
                   '  y, z\n'
                   ']\n', conf)
        self.check('---\n'
                   'a: [\n'
                   '  x,\n'
                   '  y, z]\n', conf)
        self.check('---\n'
                   'a: [\n'
                   '   x,\n'
                   '  y, z\n'
                   ']\n', conf, problem=(4, 3))
        self.check('---\n'
                   'a: [\n'
                   '  x,\n'
                   '  y, z\n'
                   '  ]\n', conf, problem=(5, 3))
        self.check('---\n'
                   'obj: {\n'
                   '  a: 1,\n'
                   '   b: 2,\n'
                   ' c: 3\n'
                   '}\n', conf, problem1=(4, 4), problem2=(5, 2))
        self.check('---\n'
                   'list: [\n'
                   '  1,\n'
                   '   2,\n'
                   ' 3\n'
                   ']\n', conf, problem1=(4, 4), problem2=(5, 2))
        self.check('---\n'
                   'top:\n'
                   '  rules: [\n'
                   '    1, 2,\n'
                   '  ]\n', conf)
        self.check('---\n'
                   'top:\n'
                   '  rules: [\n'
                   '    1, 2,\n'
                   ']\n'
                   '  rulez: [\n'
                   '    1, 2,\n'
                   '    ]\n', conf, problem1=(5, 1), problem2=(8, 5))
        self.check('---\n'
                   'top:\n'
                   '  rules:\n'
                   '    here: {\n'
                   '      foo: 1,\n'
                   '      bar: 2\n'
                   '    }\n', conf)
        self.check('---\n'
                   'top:\n'
                   '  rules:\n'
                   '    here: {\n'
                   '      foo: 1,\n'
                   '      bar: 2\n'
                   '      }\n'
                   '    there: {\n'
                   '      foo: 1,\n'
                   '      bar: 2\n'
                   '  }\n', conf, problem1=(7, 7), problem2=(11, 3))
        conf = 'indentation: {spaces: 2}'
        self.check('---\n'
                   'a: {\n'
                   '   x: 1,\n'
                   '  y, z: 1\n'
                   '}\n', conf, problem=(3, 4))
        self.check('---\n'
                   'a: [\n'
                   '   x,\n'
                   '  y, z\n'
                   ']\n', conf, problem=(3, 4))

    def test_cleared_flows(self):
        # flow:
        #   [
        #     ...
        #   ]
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   'top:\n'
                   '  rules:\n'
                   '    {\n'
                   '      foo: 1,\n'
                   '      bar: 2\n'
                   '    }\n', conf)
        self.check('---\n'
                   'top:\n'
                   '  rules:\n'
                   '    {\n'
                   '       foo: 1,\n'
                   '      bar: 2\n'
                   '    }\n', conf, problem=(5, 8))
        self.check('---\n'
                   'top:\n'
                   '  rules:\n'
                   '   {\n'
                   '     foo: 1,\n'
                   '     bar: 2\n'
                   '   }\n', conf, problem=(4, 4))
        self.check('---\n'
                   'top:\n'
                   '  rules:\n'
                   '    {\n'
                   '      foo: 1,\n'
                   '      bar: 2\n'
                   '   }\n', conf, problem=(7, 4))
        self.check('---\n'
                   'top:\n'
                   '  rules:\n'
                   '    {\n'
                   '      foo: 1,\n'
                   '      bar: 2\n'
                   '     }\n', conf, problem=(7, 6))
        self.check('---\n'
                   'top:\n'
                   '  [\n'
                   '    a, b, c\n'
                   '  ]\n', conf)
        self.check('---\n'
                   'top:\n'
                   '  [\n'
                   '     a, b, c\n'
                   '  ]\n', conf, problem=(4, 6))
        self.check('---\n'
                   'top:\n'
                   '   [\n'
                   '     a, b, c\n'
                   '   ]\n', conf, problem=(4, 6))
        self.check('---\n'
                   'top:\n'
                   '  [\n'
                   '    a, b, c\n'
                   '   ]\n', conf, problem=(5, 4))
        self.check('---\n'
                   'top:\n'
                   '  rules: [\n'
                   '    {\n'
                   '      foo: 1\n'
                   '    },\n'
                   '    {\n'
                   '      foo: 2,\n'
                   '      bar: [\n'
                   '        a, b, c\n'
                   '      ],\n'
                   '    },\n'
                   '  ]\n', conf)
        self.check('---\n'
                   'top:\n'
                   '  rules: [\n'
                   '    {\n'
                   '     foo: 1\n'
                   '     },\n'
                   '    {\n'
                   '      foo: 2,\n'
                   '        bar: [\n'
                   '          a, b, c\n'
                   '      ],\n'
                   '    },\n'
                   ']\n', conf, problem1=(5, 6), problem2=(6, 6),
                   problem3=(9, 9), problem4=(11, 7), problem5=(13, 1))

    def test_under_indented(self):
        conf = 'indentation: {spaces: 2, indent-sequences: consistent}'
        self.check('---\n'
                   'object:\n'
                   ' val: 1\n'
                   '...\n', conf, problem=(3, 2))
        self.check('---\n'
                   'object:\n'
                   '  k1:\n'
                   '   - a\n'
                   '...\n', conf, problem=(4, 4))
        self.check('---\n'
                   'object:\n'
                   '  k3:\n'
                   '    - name: Unix\n'
                   '     date: 1969\n'
                   '...\n', conf, problem=(5, 6, 'syntax'))
        conf = 'indentation: {spaces: 4, indent-sequences: consistent}'
        self.check('---\n'
                   'object:\n'
                   '   val: 1\n'
                   '...\n', conf, problem=(3, 4))
        self.check('---\n'
                   '- el1\n'
                   '- el2:\n'
                   '   - subel\n'
                   '...\n', conf, problem=(4, 4))
        self.check('---\n'
                   'object:\n'
                   '    k3:\n'
                   '        - name: Linux\n'
                   '         date: 1991\n'
                   '...\n', conf, problem=(5, 10, 'syntax'))
        conf = 'indentation: {spaces: 2, indent-sequences: true}'
        self.check('---\n'
                   'a:\n'
                   '-\n'  # empty list
                   'b: c\n'
                   '...\n', conf, problem=(3, 1))
        conf = 'indentation: {spaces: 2, indent-sequences: consistent}'
        self.check('---\n'
                   'a:\n'
                   '  -\n'  # empty list
                   'b:\n'
                   '-\n'
                   'c: d\n'
                   '...\n', conf, problem=(5, 1))

    def test_over_indented(self):
        conf = 'indentation: {spaces: 2, indent-sequences: consistent}'
        self.check('---\n'
                   'object:\n'
                   '   val: 1\n'
                   '...\n', conf, problem=(3, 4))
        self.check('---\n'
                   'object:\n'
                   '  k1:\n'
                   '     - a\n'
                   '...\n', conf, problem=(4, 6))
        self.check('---\n'
                   'object:\n'
                   '  k3:\n'
                   '    - name: Unix\n'
                   '       date: 1969\n'
                   '...\n', conf, problem=(5, 12, 'syntax'))
        conf = 'indentation: {spaces: 4, indent-sequences: consistent}'
        self.check('---\n'
                   'object:\n'
                   '     val: 1\n'
                   '...\n', conf, problem=(3, 6))
        self.check('---\n'
                   ' object:\n'
                   '     val: 1\n'
                   '...\n', conf, problem=(2, 2))
        self.check('---\n'
                   '- el1\n'
                   '- el2:\n'
                   '     - subel\n'
                   '...\n', conf, problem=(4, 6))
        self.check('---\n'
                   '- el1\n'
                   '- el2:\n'
                   '              - subel\n'
                   '...\n', conf, problem=(4, 15))
        self.check('---\n'
                   '  - el1\n'
                   '  - el2:\n'
                   '        - subel\n'
                   '...\n', conf,
                   problem=(2, 3))
        self.check('---\n'
                   'object:\n'
                   '    k3:\n'
                   '        - name: Linux\n'
                   '           date: 1991\n'
                   '...\n', conf, problem=(5, 16, 'syntax'))
        conf = 'indentation: {spaces: 4, indent-sequences: whatever}'
        self.check('---\n'
                   '  - el1\n'
                   '  - el2:\n'
                   '    - subel\n'
                   '...\n', conf,
                   problem=(2, 3))
        conf = 'indentation: {spaces: 2, indent-sequences: false}'
        self.check('---\n'
                   'a:\n'
                   '  -\n'  # empty list
                   'b: c\n'
                   '...\n', conf, problem=(3, 3))
        conf = 'indentation: {spaces: 2, indent-sequences: consistent}'
        self.check('---\n'
                   'a:\n'
                   '-\n'  # empty list
                   'b:\n'
                   '  -\n'
                   'c: d\n'
                   '...\n', conf, problem=(5, 3))

    def test_multi_lines(self):
        conf = 'indentation: {spaces: consistent, indent-sequences: true}'
        self.check('---\n'
                   'long_string: >\n'
                   '  bla bla blah\n'
                   '  blah bla bla\n'
                   '...\n', conf)
        self.check('---\n'
                   '- long_string: >\n'
                   '    bla bla blah\n'
                   '    blah bla bla\n'
                   '...\n', conf)
        self.check('---\n'
                   'obj:\n'
                   '  - long_string: >\n'
                   '      bla bla blah\n'
                   '      blah bla bla\n'
                   '...\n', conf)

    def test_empty_value(self):
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   'key1:\n'
                   'key2: not empty\n'
                   'key3:\n'
                   '...\n', conf)
        self.check('---\n'
                   '-\n'
                   '- item 2\n'
                   '-\n'
                   '...\n', conf)

    def test_nested_collections(self):
        conf = 'indentation: {spaces: 2}'
        self.check('---\n'
                   '- o:\n'
                   '  k1: v1\n'
                   '...\n', conf)
        self.check('---\n'
                   '- o:\n'
                   ' k1: v1\n'
                   '...\n', conf, problem=(3, 2, 'syntax'))
        self.check('---\n'
                   '- o:\n'
                   '   k1: v1\n'
                   '...\n', conf, problem=(3, 4))
        conf = 'indentation: {spaces: 4}'
        self.check('---\n'
                   '- o:\n'
                   '      k1: v1\n'
                   '...\n', conf)
        self.check('---\n'
                   '- o:\n'
                   '     k1: v1\n'
                   '...\n', conf, problem=(3, 6))
        self.check('---\n'
                   '- o:\n'
                   '       k1: v1\n'
                   '...\n', conf, problem=(3, 8))
        self.check('---\n'
                   '- - - - item\n'
                   '    - elem 1\n'
                   '    - elem 2\n'
                   '    - - - - - very nested: a\n'
                   '              key: value\n'
                   '...\n', conf)
        self.check('---\n'
                   ' - - - - item\n'
                   '     - elem 1\n'
                   '     - elem 2\n'
                   '     - - - - - very nested: a\n'
                   '               key: value\n'
                   '...\n', conf, problem=(2, 2))

    def test_return(self):
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   'a:\n'
                   '  b:\n'
                   '    c:\n'
                   '  d:\n'
                   '    e:\n'
                   '      f:\n'
                   'g:\n'
                   '...\n', conf)
        self.check('---\n'
                   'a:\n'
                   '  b:\n'
                   '    c:\n'
                   '   d:\n'
                   '...\n', conf, problem=(5, 4, 'syntax'))
        self.check('---\n'
                   'a:\n'
                   '  b:\n'
                   '    c:\n'
                   ' d:\n'
                   '...\n', conf, problem=(5, 2, 'syntax'))

    def test_first_line(self):
        conf = ('indentation: {spaces: consistent}\n'
                'document-start: disable\n')
        self.check('  a: 1\n', conf, problem=(1, 3))

    def test_explicit_block_mappings(self):
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   'object:\n'
                   '    ? key\n'
                   '    : value\n', conf)
        self.check('---\n'
                   'object:\n'
                   '    ? key\n'
                   '    :\n'
                   '        value\n'
                   '...\n', conf)
        self.check('---\n'
                   'object:\n'
                   '    ?\n'
                   '        key\n'
                   '    : value\n', conf)
        self.check('---\n'
                   'object:\n'
                   '    ?\n'
                   '        key\n'
                   '    :\n'
                   '        value\n'
                   '...\n', conf)
        self.check('---\n'
                   '- ? key\n'
                   '  : value\n', conf)
        self.check('---\n'
                   '- ? key\n'
                   '  :\n'
                   '      value\n'
                   '...\n', conf)
        self.check('---\n'
                   '- ?\n'
                   '      key\n'
                   '  : value\n', conf)
        self.check('---\n'
                   '- ?\n'
                   '      key\n'
                   '  :\n'
                   '      value\n'
                   '...\n', conf)
        self.check('---\n'
                   'object:\n'
                   '    ? key\n'
                   '    :\n'
                   '       value\n'
                   '...\n', conf, problem=(5, 8))
        self.check('---\n'
                   '- - ?\n'
                   '       key\n'
                   '    :\n'
                   '      value\n'
                   '...\n', conf, problem=(5, 7))
        self.check('---\n'
                   'object:\n'
                   '    ?\n'
                   '       key\n'
                   '    :\n'
                   '         value\n'
                   '...\n', conf, problem1=(4, 8), problem2=(6, 10))
        self.check('---\n'
                   'object:\n'
                   '    ?\n'
                   '         key\n'
                   '    :\n'
                   '       value\n'
                   '...\n', conf, problem1=(4, 10), problem2=(6, 8))

    def test_clear_sequence_item(self):
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   '-\n'
                   '  string\n'
                   '-\n'
                   '  map: ping\n'
                   '-\n'
                   '  - sequence\n'
                   '  -\n'
                   '    nested\n'
                   '  -\n'
                   '    >\n'
                   '      multi\n'
                   '      line\n'
                   '...\n', conf)
        self.check('---\n'
                   '-\n'
                   ' string\n'
                   '-\n'
                   '   string\n', conf, problem=(5, 4))
        self.check('---\n'
                   '-\n'
                   ' map: ping\n'
                   '-\n'
                   '   map: ping\n', conf, problem=(5, 4))
        self.check('---\n'
                   '-\n'
                   ' - sequence\n'
                   '-\n'
                   '   - sequence\n', conf, problem=(5, 4))
        self.check('---\n'
                   '-\n'
                   '  -\n'
                   '   nested\n'
                   '  -\n'
                   '     nested\n', conf, problem1=(4, 4), problem2=(6, 6))
        self.check('---\n'
                   '-\n'
                   '  -\n'
                   '     >\n'
                   '      multi\n'
                   '      line\n'
                   '...\n', conf, problem=(4, 6))
        conf = 'indentation: {spaces: 2}'
        self.check('---\n'
                   '-\n'
                   ' string\n'
                   '-\n'
                   '   string\n', conf, problem1=(3, 2), problem2=(5, 4))
        self.check('---\n'
                   '-\n'
                   ' map: ping\n'
                   '-\n'
                   '   map: ping\n', conf, problem1=(3, 2), problem2=(5, 4))
        self.check('---\n'
                   '-\n'
                   ' - sequence\n'
                   '-\n'
                   '   - sequence\n', conf, problem1=(3, 2), problem2=(5, 4))
        self.check('---\n'
                   '-\n'
                   '  -\n'
                   '   nested\n'
                   '  -\n'
                   '     nested\n', conf, problem1=(4, 4), problem2=(6, 6))

    def test_anchors(self):
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   'key: &anchor value\n', conf)
        self.check('---\n'
                   'key: &anchor\n'
                   '  value\n', conf)
        self.check('---\n'
                   '- &anchor value\n', conf)
        self.check('---\n'
                   '- &anchor\n'
                   '  value\n', conf)
        self.check('---\n'
                   'key: &anchor [1,\n'
                   '              2]\n', conf)
        self.check('---\n'
                   'key: &anchor\n'
                   '  [1,\n'
                   '   2]\n', conf)
        self.check('---\n'
                   'key: &anchor\n'
                   '  - 1\n'
                   '  - 2\n', conf)
        self.check('---\n'
                   '- &anchor [1,\n'
                   '           2]\n', conf)
        self.check('---\n'
                   '- &anchor\n'
                   '  [1,\n'
                   '   2]\n', conf)
        self.check('---\n'
                   '- &anchor\n'
                   '  - 1\n'
                   '  - 2\n', conf)
        self.check('---\n'
                   'key:\n'
                   '  &anchor1\n'
                   '  value\n', conf)
        self.check('---\n'
                   'pre:\n'
                   '  &anchor1 0\n'
                   '&anchor2 key:\n'
                   '  value\n', conf)
        self.check('---\n'
                   'machine0:\n'
                   '  /etc/hosts: &ref-etc-hosts\n'
                   '    content:\n'
                   '      - 127.0.0.1: localhost\n'
                   '      - ::1: localhost\n'
                   '    mode: 0644\n'
                   'machine1:\n'
                   '  /etc/hosts: *ref-etc-hosts\n', conf)
        self.check('---\n'
                   'list:\n'
                   '  - k: v\n'
                   '  - &a truc\n'
                   '  - &b\n'
                   '    truc\n'
                   '  - k: *a\n', conf)

    def test_tags(self):
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   '-\n'
                   '  "flow in block"\n'
                   '- >\n'
                   '    Block scalar\n'
                   '- !!map  # Block collection\n'
                   '  foo: bar\n', conf)

        conf = 'indentation: {spaces: consistent, indent-sequences: false}'
        self.check('---\n'
                   'sequence: !!seq\n'
                   '- entry\n'
                   '- !!seq\n'
                   '  - nested\n', conf)
        self.check('---\n'
                   'mapping: !!map\n'
                   '  foo: bar\n'
                   'Block style: !!map\n'
                   '  Clark: Evans\n'
                   '  Ingy: döt Net\n'
                   '  Oren: Ben-Kiki\n', conf)
        self.check('---\n'
                   'Flow style: !!map {Clark: Evans, Ingy: döt Net}\n'
                   'Block style: !!seq\n'
                   '- Clark Evans\n'
                   '- Ingy döt Net\n', conf)

    def test_flows_imbrication(self):
        conf = 'indentation: {spaces: consistent}'
        self.check('---\n'
                   '[val]: value\n', conf)
        self.check('---\n'
                   '{key}: value\n', conf)
        self.check('---\n'
                   '{key: val}: value\n', conf)
        self.check('---\n'
                   '[[val]]: value\n', conf)
        self.check('---\n'
                   '{{key}}: value\n', conf)
        self.check('---\n'
                   '{{key: val1}: val2}: value\n', conf)
        self.check('---\n'
                   '- [val, {{key: val}: val}]: value\n'
                   '- {[val,\n'
                   '    {{key: val}: val}]}\n'
                   '- {[val,\n'
                   '    {{key: val,\n'
                   '      key2}}]}\n'
                   '- {{{{{moustaches}}}}}\n'
                   '- {{{{{moustache,\n'
                   '       moustache},\n'
                   '      moustache}},\n'
                   '    moustache}}\n', conf)
        self.check('---\n'
                   '- {[val,\n'
                   '     {{key: val}: val}]}\n',
                   conf, problem=(3, 6))
        self.check('---\n'
                   '- {[val,\n'
                   '    {{key: val,\n'
                   '     key2}}]}\n',
                   conf, problem=(4, 6))
        self.check('---\n'
                   '- {{{{{moustache,\n'
                   '       moustache},\n'
                   '       moustache}},\n'
                   '   moustache}}\n',
                   conf, problem1=(4, 8), problem2=(5, 4))


class ScalarIndentationTestCase(RuleTestCase):
    rule_id = 'indentation'

    def test_basics_plain(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: false}\n'
                'document-start: disable\n')
        self.check('multi\n'
                   'line\n', conf)
        self.check('multi\n'
                   ' line\n', conf)
        self.check('- multi\n'
                   '  line\n', conf)
        self.check('- multi\n'
                   '   line\n', conf)
        self.check('a key: multi\n'
                   '       line\n', conf)
        self.check('a key: multi\n'
                   '  line\n', conf)
        self.check('a key: multi\n'
                   '        line\n', conf)
        self.check('a key:\n'
                   '  multi\n'
                   '  line\n', conf)
        self.check('- C code: void main() {\n'
                   '              printf("foo");\n'
                   '          }\n', conf)
        self.check('- C code:\n'
                   '    void main() {\n'
                   '        printf("foo");\n'
                   '    }\n', conf)

    def test_check_multi_line_plain(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('multi\n'
                   ' line\n', conf, problem=(2, 2))
        self.check('- multi\n'
                   '   line\n', conf, problem=(2, 4))
        self.check('a key: multi\n'
                   '  line\n', conf, problem=(2, 3))
        self.check('a key: multi\n'
                   '        line\n', conf, problem=(2, 9))
        self.check('a key:\n'
                   '  multi\n'
                   '   line\n', conf, problem=(3, 4))
        self.check('- C code: void main() {\n'
                   '              printf("foo");\n'
                   '          }\n', conf, problem=(2, 15))
        self.check('- C code:\n'
                   '    void main() {\n'
                   '        printf("foo");\n'
                   '    }\n', conf, problem=(3, 9))

    def test_basics_quoted(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: false}\n'
                'document-start: disable\n')
        self.check('"multi\n'
                   ' line"\n', conf)
        self.check('- "multi\n'
                   '   line"\n', conf)
        self.check('a key: "multi\n'
                   '        line"\n', conf)
        self.check('a key:\n'
                   '  "multi\n'
                   '   line"\n', conf)
        self.check('- jinja2: "{% if ansible is defined %}\n'
                   '             {{ ansible }}\n'
                   '           {% else %}\n'
                   '             {{ chef }}\n'
                   '           {% endif %}"\n', conf)
        self.check('- jinja2:\n'
                   '    "{% if ansible is defined %}\n'
                   '       {{ ansible }}\n'
                   '     {% else %}\n'
                   '       {{ chef }}\n'
                   '     {% endif %}"\n', conf)
        self.check('["this is a very long line\n'
                   '  that needs to be split",\n'
                   ' "other line"]\n', conf)
        self.check('["multi\n'
                   '  line 1", "multi\n'
                   '            line 2"]\n', conf)

    def test_check_multi_line_quoted(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('"multi\n'
                   'line"\n', conf, problem=(2, 1))
        self.check('"multi\n'
                   '  line"\n', conf, problem=(2, 3))
        self.check('- "multi\n'
                   '  line"\n', conf, problem=(2, 3))
        self.check('- "multi\n'
                   '    line"\n', conf, problem=(2, 5))
        self.check('a key: "multi\n'
                   '  line"\n', conf, problem=(2, 3))
        self.check('a key: "multi\n'
                   '       line"\n', conf, problem=(2, 8))
        self.check('a key: "multi\n'
                   '         line"\n', conf, problem=(2, 10))
        self.check('a key:\n'
                   '  "multi\n'
                   '  line"\n', conf, problem=(3, 3))
        self.check('a key:\n'
                   '  "multi\n'
                   '    line"\n', conf, problem=(3, 5))
        self.check('- jinja2: "{% if ansible is defined %}\n'
                   '             {{ ansible }}\n'
                   '           {% else %}\n'
                   '             {{ chef }}\n'
                   '           {% endif %}"\n', conf,
                   problem1=(2, 14), problem2=(4, 14))
        self.check('- jinja2:\n'
                   '    "{% if ansible is defined %}\n'
                   '       {{ ansible }}\n'
                   '     {% else %}\n'
                   '       {{ chef }}\n'
                   '     {% endif %}"\n', conf,
                   problem1=(3, 8), problem2=(5, 8))
        self.check('["this is a very long line\n'
                   '  that needs to be split",\n'
                   ' "other line"]\n', conf)
        self.check('["this is a very long line\n'
                   ' that needs to be split",\n'
                   ' "other line"]\n', conf, problem=(2, 2))
        self.check('["this is a very long line\n'
                   '   that needs to be split",\n'
                   ' "other line"]\n', conf, problem=(2, 4))
        self.check('["multi\n'
                   '  line 1", "multi\n'
                   '            line 2"]\n', conf)
        self.check('["multi\n'
                   '  line 1", "multi\n'
                   '           line 2"]\n', conf, problem=(3, 12))
        self.check('["multi\n'
                   '  line 1", "multi\n'
                   '             line 2"]\n', conf, problem=(3, 14))

    def test_basics_folded_style(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: false}\n'
                'document-start: disable\n')
        self.check('>\n'
                   '  multi\n'
                   '  line\n', conf)
        self.check('- >\n'
                   '    multi\n'
                   '    line\n', conf)
        self.check('- key: >\n'
                   '    multi\n'
                   '    line\n', conf)
        self.check('- key:\n'
                   '    >\n'
                   '      multi\n'
                   '      line\n', conf)
        self.check('- ? >\n'
                   '      multi-line\n'
                   '      key\n'
                   '  : >\n'
                   '      multi-line\n'
                   '      value\n', conf)
        self.check('- ?\n'
                   '    >\n'
                   '      multi-line\n'
                   '      key\n'
                   '  :\n'
                   '    >\n'
                   '      multi-line\n'
                   '      value\n', conf)
        self.check('- jinja2: >\n'
                   '    {% if ansible is defined %}\n'
                   '      {{ ansible }}\n'
                   '    {% else %}\n'
                   '      {{ chef }}\n'
                   '    {% endif %}\n', conf)

    def test_check_multi_line_folded_style(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('>\n'
                   '  multi\n'
                   '   line\n', conf, problem=(3, 4))
        self.check('- >\n'
                   '    multi\n'
                   '     line\n', conf, problem=(3, 6))
        self.check('- key: >\n'
                   '    multi\n'
                   '     line\n', conf, problem=(3, 6))
        self.check('- key:\n'
                   '    >\n'
                   '      multi\n'
                   '       line\n', conf, problem=(4, 8))
        self.check('- ? >\n'
                   '      multi-line\n'
                   '       key\n'
                   '  : >\n'
                   '      multi-line\n'
                   '       value\n', conf,
                   problem1=(3, 8), problem2=(6, 8))
        self.check('- ?\n'
                   '    >\n'
                   '      multi-line\n'
                   '       key\n'
                   '  :\n'
                   '    >\n'
                   '      multi-line\n'
                   '       value\n', conf,
                   problem1=(4, 8), problem2=(8, 8))
        self.check('- jinja2: >\n'
                   '    {% if ansible is defined %}\n'
                   '      {{ ansible }}\n'
                   '    {% else %}\n'
                   '      {{ chef }}\n'
                   '    {% endif %}\n', conf,
                   problem1=(3, 7), problem2=(5, 7))

    def test_basics_literal_style(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: false}\n'
                'document-start: disable\n')
        self.check('|\n'
                   '  multi\n'
                   '  line\n', conf)
        self.check('- |\n'
                   '    multi\n'
                   '    line\n', conf)
        self.check('- key: |\n'
                   '    multi\n'
                   '    line\n', conf)
        self.check('- key:\n'
                   '    |\n'
                   '      multi\n'
                   '      line\n', conf)
        self.check('- ? |\n'
                   '      multi-line\n'
                   '      key\n'
                   '  : |\n'
                   '      multi-line\n'
                   '      value\n', conf)
        self.check('- ?\n'
                   '    |\n'
                   '      multi-line\n'
                   '      key\n'
                   '  :\n'
                   '    |\n'
                   '      multi-line\n'
                   '      value\n', conf)
        self.check('- jinja2: |\n'
                   '    {% if ansible is defined %}\n'
                   '     {{ ansible }}\n'
                   '    {% else %}\n'
                   '      {{ chef }}\n'
                   '    {% endif %}\n', conf)

    def test_check_multi_line_literal_style(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('|\n'
                   '  multi\n'
                   '   line\n', conf, problem=(3, 4))
        self.check('- |\n'
                   '    multi\n'
                   '     line\n', conf, problem=(3, 6))
        self.check('- key: |\n'
                   '    multi\n'
                   '     line\n', conf, problem=(3, 6))
        self.check('- key:\n'
                   '    |\n'
                   '      multi\n'
                   '       line\n', conf, problem=(4, 8))
        self.check('- ? |\n'
                   '      multi-line\n'
                   '       key\n'
                   '  : |\n'
                   '      multi-line\n'
                   '       value\n', conf,
                   problem1=(3, 8), problem2=(6, 8))
        self.check('- ?\n'
                   '    |\n'
                   '      multi-line\n'
                   '       key\n'
                   '  :\n'
                   '    |\n'
                   '      multi-line\n'
                   '       value\n', conf,
                   problem1=(4, 8), problem2=(8, 8))
        self.check('- jinja2: |\n'
                   '    {% if ansible is defined %}\n'
                   '      {{ ansible }}\n'
                   '    {% else %}\n'
                   '      {{ chef }}\n'
                   '    {% endif %}\n', conf,
                   problem1=(3, 7), problem2=(5, 7))

    # The following "paragraph" examples are inspired from
    # http://stackoverflow.com/questions/3790454/in-yaml-how-do-i-break-a-string-over-multiple-lines

    def test_paragraph_plain(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('- long text: very "long"\n'
                   '             \'string\' with\n'
                   '\n'
                   '             paragraph gap, \\n and\n'
                   '             spaces.\n', conf)
        self.check('- long text: very "long"\n'
                   '    \'string\' with\n'
                   '\n'
                   '    paragraph gap, \\n and\n'
                   '    spaces.\n', conf,
                   problem1=(2, 5), problem2=(4, 5), problem3=(5, 5))
        self.check('- long text:\n'
                   '    very "long"\n'
                   '    \'string\' with\n'
                   '\n'
                   '    paragraph gap, \\n and\n'
                   '    spaces.\n', conf)

    def test_paragraph_double_quoted(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('- long text: "very \\"long\\"\n'
                   '              \'string\' with\n'
                   '\n'
                   '              paragraph gap, \\n and\n'
                   '              spaces."\n', conf)
        self.check('- long text: "very \\"long\\"\n'
                   '    \'string\' with\n'
                   '\n'
                   '    paragraph gap, \\n and\n'
                   '    spaces."\n', conf,
                   problem1=(2, 5), problem2=(4, 5), problem3=(5, 5))
        self.check('- long text: "very \\"long\\"\n'
                   '\'string\' with\n'
                   '\n'
                   'paragraph gap, \\n and\n'
                   'spaces."\n', conf,
                   problem1=(2, 1), problem2=(4, 1), problem3=(5, 1))
        self.check('- long text:\n'
                   '    "very \\"long\\"\n'
                   '     \'string\' with\n'
                   '\n'
                   '     paragraph gap, \\n and\n'
                   '     spaces."\n', conf)

    def test_paragraph_single_quoted(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('- long text: \'very "long"\n'
                   '              \'\'string\'\' with\n'
                   '\n'
                   '              paragraph gap, \\n and\n'
                   '              spaces.\'\n', conf)
        self.check('- long text: \'very "long"\n'
                   '    \'\'string\'\' with\n'
                   '\n'
                   '    paragraph gap, \\n and\n'
                   '    spaces.\'\n', conf,
                   problem1=(2, 5), problem2=(4, 5), problem3=(5, 5))
        self.check('- long text: \'very "long"\n'
                   '\'\'string\'\' with\n'
                   '\n'
                   'paragraph gap, \\n and\n'
                   'spaces.\'\n', conf,
                   problem1=(2, 1), problem2=(4, 1), problem3=(5, 1))
        self.check('- long text:\n'
                   '    \'very "long"\n'
                   '     \'\'string\'\' with\n'
                   '\n'
                   '     paragraph gap, \\n and\n'
                   '     spaces.\'\n', conf)

    def test_paragraph_folded(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('- long text: >\n'
                   '    very "long"\n'
                   '    \'string\' with\n'
                   '\n'
                   '    paragraph gap, \\n and\n'
                   '    spaces.\n', conf)
        self.check('- long text: >\n'
                   '    very "long"\n'
                   '     \'string\' with\n'
                   '\n'
                   '      paragraph gap, \\n and\n'
                   '       spaces.\n', conf,
                   problem1=(3, 6), problem2=(5, 7), problem3=(6, 8))

    def test_paragraph_literal(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('- long text: |\n'
                   '    very "long"\n'
                   '    \'string\' with\n'
                   '\n'
                   '    paragraph gap, \\n and\n'
                   '    spaces.\n', conf)
        self.check('- long text: |\n'
                   '    very "long"\n'
                   '     \'string\' with\n'
                   '\n'
                   '      paragraph gap, \\n and\n'
                   '       spaces.\n', conf,
                   problem1=(3, 6), problem2=(5, 7), problem3=(6, 8))

    def test_consistent(self):
        conf = ('indentation: {spaces: consistent,\n'
                '              check-multi-line-strings: true}\n'
                'document-start: disable\n')
        self.check('multi\n'
                   'line\n', conf)
        self.check('multi\n'
                   ' line\n', conf, problem=(2, 2))
        self.check('- multi\n'
                   '  line\n', conf)
        self.check('- multi\n'
                   '   line\n', conf, problem=(2, 4))
        self.check('a key: multi\n'
                   '  line\n', conf, problem=(2, 3))
        self.check('a key: multi\n'
                   '        line\n', conf, problem=(2, 9))
        self.check('a key:\n'
                   '  multi\n'
                   '   line\n', conf, problem=(3, 4))
        self.check('- C code: void main() {\n'
                   '              printf("foo");\n'
                   '          }\n', conf, problem=(2, 15))
        self.check('- C code:\n'
                   '    void main() {\n'
                   '        printf("foo");\n'
                   '    }\n', conf, problem=(3, 9))
        self.check('>\n'
                   '  multi\n'
                   '  line\n', conf)
        self.check('>\n'
                   '     multi\n'
                   '     line\n', conf)
        self.check('>\n'
                   '     multi\n'
                   '      line\n', conf, problem=(3, 7))
