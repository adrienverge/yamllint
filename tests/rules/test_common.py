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

from yamllint.rules.common import (Comment, get_line_indent,
                                   get_comments_between_tokens)


class CommonTestCase(unittest.TestCase):
    def test_get_line_indent(self):
        tokens = list(yaml.scan('a: 1\n'
                                'b:\n'
                                '  - c: [2, 3, {d: 4}]\n'))

        self.assertEqual(tokens[3].value, 'a')
        self.assertEqual(tokens[5].value, '1')
        self.assertEqual(tokens[7].value, 'b')
        self.assertEqual(tokens[13].value, 'c')
        self.assertEqual(tokens[16].value, '2')
        self.assertEqual(tokens[18].value, '3')
        self.assertEqual(tokens[22].value, 'd')
        self.assertEqual(tokens[24].value, '4')

        for i in (3, 5):
            self.assertEqual(get_line_indent(tokens[i]), 0)
        for i in (7,):
            self.assertEqual(get_line_indent(tokens[i]), 0)
        for i in (13, 16, 18, 22, 24):
            self.assertEqual(get_line_indent(tokens[i]), 2)

    def check_comments(self, buffer, *expected):
        yaml_loader = yaml.BaseLoader(buffer)

        comments = []

        next = yaml_loader.peek_token()
        while next is not None:
            curr = yaml_loader.get_token()
            next = yaml_loader.peek_token()
            for comment in get_comments_between_tokens(curr, next):
                comments.append(comment)

        self.assertEqual(comments, list(expected))

    def test_get_comments_between_tokens(self):
        self.check_comments('# comment\n',
                            Comment(1, 1, '# comment', 0))
        self.check_comments('---\n'
                            '# comment\n'
                            '...\n',
                            Comment(2, 1, '# comment', 0))
        self.check_comments('---\n'
                            '# no newline char',
                            Comment(2, 1, '# no newline char', 0))
        self.check_comments('# just comment',
                            Comment(1, 1, '# just comment', 0))
        self.check_comments('\n'
                            '   # indented comment\n',
                            Comment(2, 4, '# indented comment', 0))
        self.check_comments('\n'
                            '# trailing spaces    \n',
                            Comment(2, 1, '# trailing spaces    ', 0))
        self.check_comments('# comment one\n'
                            '\n'
                            'key: val  # key=val\n'
                            '\n'
                            '# this is\n'
                            '# a block     \n'
                            '# comment\n'
                            '\n'
                            'other:\n'
                            '  - foo  # equals\n'
                            '         # bar\n',
                            Comment(1, 1, '# comment one', 0),
                            Comment(3, 11, '# key=val', 0),
                            Comment(5, 1, '# this is', 0),
                            Comment(6, 1, '# a block     ', 0),
                            Comment(7, 1, '# comment', 0),
                            Comment(10, 10, '# equals', 0),
                            Comment(11, 10, '# bar', 0))
