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

import unittest

import yaml

from yamllint.parser import (line_generator, token_generator,
                             token_or_line_generator, Line, Token)


class ParserTestCase(unittest.TestCase):
    def test_line_generator(self):
        e = list(line_generator(''))
        self.assertEqual(len(e), 1)
        self.assertEqual(e[0].line_no, 1)
        self.assertEqual(e[0].start, 0)
        self.assertEqual(e[0].end, 0)

        e = list(line_generator('\n'))
        self.assertEqual(len(e), 2)

        e = list(line_generator(' \n'))
        self.assertEqual(len(e), 2)
        self.assertEqual(e[0].line_no, 1)
        self.assertEqual(e[0].start, 0)
        self.assertEqual(e[0].end, 1)

        e = list(line_generator('\n\n'))
        self.assertEqual(len(e), 3)

        e = list(line_generator('---\n'
                                'this is line 1\n'
                                'line 2\n'
                                '\n'
                                '3\n'))
        self.assertEqual(len(e), 6)
        self.assertEqual(e[0].line_no, 1)
        self.assertEqual(e[0].content, '---')
        self.assertEqual(e[2].content, 'line 2')
        self.assertEqual(e[3].content, '')
        self.assertEqual(e[5].line_no, 6)

        e = list(line_generator('test with\n'
                                'no newline\n'
                                'at the end'))
        self.assertEqual(len(e), 3)
        self.assertEqual(e[2].line_no, 3)
        self.assertEqual(e[2].content, 'at the end')

    def test_token_generator(self):
        e = list(token_generator(''))
        self.assertEqual(len(e), 2)
        self.assertEqual(e[0].prev, None)
        self.assertIsInstance(e[0].curr, yaml.Token)
        self.assertIsInstance(e[0].next, yaml.Token)
        self.assertEqual(e[1].prev, e[0].curr)
        self.assertEqual(e[1].curr, e[0].next)
        self.assertEqual(e[1].next, None)

        e = list(token_generator('---\n'
                                 'k: v\n'))
        self.assertEqual(len(e), 9)
        self.assertIsInstance(e[3].curr, yaml.KeyToken)
        self.assertIsInstance(e[5].curr, yaml.ValueToken)

    def test_token_or_line_generator(self):
        e = list(token_or_line_generator('---\n'
                                         'k: v\n'))
        self.assertEqual(len(e), 12)
        self.assertIsInstance(e[0], Token)
        self.assertIsInstance(e[0].curr, yaml.StreamStartToken)
        self.assertIsInstance(e[1], Token)
        self.assertIsInstance(e[1].curr, yaml.DocumentStartToken)
        self.assertIsInstance(e[2], Line)
        self.assertIsInstance(e[3].curr, yaml.BlockMappingStartToken)
        self.assertIsInstance(e[4].curr, yaml.KeyToken)
        self.assertIsInstance(e[6].curr, yaml.ValueToken)
        self.assertIsInstance(e[8], Line)
        self.assertIsInstance(e[11], Line)
