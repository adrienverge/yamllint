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

from yamllint.parser import (line_generator, token_or_comment_generator,
                             token_or_comment_or_line_generator,
                             Line, Token, Comment)


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

    def test_token_or_comment_generator(self):
        e = list(token_or_comment_generator(''))
        self.assertEqual(len(e), 2)
        self.assertIsNone(e[0].prev)
        self.assertIsInstance(e[0].curr, yaml.Token)
        self.assertIsInstance(e[0].next, yaml.Token)
        self.assertEqual(e[1].prev, e[0].curr)
        self.assertEqual(e[1].curr, e[0].next)
        self.assertIsNone(e[1].next)

        e = list(token_or_comment_generator('---\n'
                                            'k: v\n'))
        self.assertEqual(len(e), 9)
        self.assertIsInstance(e[3].curr, yaml.KeyToken)
        self.assertIsInstance(e[5].curr, yaml.ValueToken)

        e = list(token_or_comment_generator('# start comment\n'
                                            '- a\n'
                                            '- key: val  # key=val\n'
                                            '# this is\n'
                                            '# a block     \n'
                                            '# comment\n'
                                            '- c\n'
                                            '# end comment\n'))
        self.assertEqual(len(e), 21)
        self.assertIsInstance(e[1], Comment)
        self.assertEqual(e[1], Comment(1, 1, '# start comment', 0))
        self.assertEqual(e[11], Comment(3, 13, '# key=val', 0))
        self.assertEqual(e[12], Comment(4, 1, '# this is', 0))
        self.assertEqual(e[13], Comment(5, 1, '# a block     ', 0))
        self.assertEqual(e[14], Comment(6, 1, '# comment', 0))
        self.assertEqual(e[18], Comment(8, 1, '# end comment', 0))

        e = list(token_or_comment_generator('---\n'
                                            '# no newline char'))
        self.assertEqual(e[2], Comment(2, 1, '# no newline char', 0))

        e = list(token_or_comment_generator('# just comment'))
        self.assertEqual(e[1], Comment(1, 1, '# just comment', 0))

        e = list(token_or_comment_generator('\n'
                                            '   # indented comment\n'))
        self.assertEqual(e[1], Comment(2, 4, '# indented comment', 0))

        e = list(token_or_comment_generator('\n'
                                            '# trailing spaces    \n'))
        self.assertEqual(e[1], Comment(2, 1, '# trailing spaces    ', 0))

        e = [c for c in
             token_or_comment_generator('# block\n'
                                        '# comment\n'
                                        '- data   # inline comment\n'
                                        '# block\n'
                                        '# comment\n'
                                        '- k: v   # inline comment\n'
                                        '- [ l, ist\n'
                                        ']   # inline comment\n'
                                        '- { m: ap\n'
                                        '}   # inline comment\n'
                                        '# block comment\n'
                                        '- data   # inline comment\n')
             if isinstance(c, Comment)]
        self.assertEqual(len(e), 10)
        self.assertFalse(e[0].is_inline())
        self.assertFalse(e[1].is_inline())
        self.assertTrue(e[2].is_inline())
        self.assertFalse(e[3].is_inline())
        self.assertFalse(e[4].is_inline())
        self.assertTrue(e[5].is_inline())
        self.assertTrue(e[6].is_inline())
        self.assertTrue(e[7].is_inline())
        self.assertFalse(e[8].is_inline())
        self.assertTrue(e[9].is_inline())

    def test_token_or_comment_or_line_generator(self):
        e = list(token_or_comment_or_line_generator('---\n'
                                                    'k: v  # k=v\n'))
        self.assertEqual(len(e), 13)
        self.assertIsInstance(e[0], Token)
        self.assertIsInstance(e[0].curr, yaml.StreamStartToken)
        self.assertIsInstance(e[1], Token)
        self.assertIsInstance(e[1].curr, yaml.DocumentStartToken)
        self.assertIsInstance(e[2], Line)
        self.assertIsInstance(e[3].curr, yaml.BlockMappingStartToken)
        self.assertIsInstance(e[4].curr, yaml.KeyToken)
        self.assertIsInstance(e[6].curr, yaml.ValueToken)
        self.assertIsInstance(e[8], Comment)
        self.assertIsInstance(e[9], Line)
        self.assertIsInstance(e[12], Line)
