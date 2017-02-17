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


class ColonTestCase(RuleTestCase):
    rule_id = 'braces'

    def test_disabled(self):
        conf = 'braces: disable'
        self.check('---\n'
                   'dict1: {}\n'
                   'dict2: { }\n'
                   'dict3: {   a: 1, b}\n'
                   'dict4: {a: 1, b, c: 3 }\n'
                   'dict5: {a: 1, b, c: 3 }\n'
                   'dict6: {  a: 1, b, c: 3 }\n'
                   'dict7: {   a: 1, b, c: 3 }\n', conf)

    def test_min_spaces(self):
        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: 0\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'dict: {}\n', conf)

        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: 1\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'dict: {}\n', conf, problem=(2, 8))
        self.check('---\n'
                   'dict: { }\n', conf)
        self.check('---\n'
                   'dict: {a: 1, b}\n', conf,
                   problem1=(2, 8), problem2=(2, 15))
        self.check('---\n'
                   'dict: { a: 1, b }\n', conf)
        self.check('---\n'
                   'dict: {\n'
                   '  a: 1,\n'
                   '  b\n'
                   '}\n', conf)

        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: 3\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'dict: { a: 1, b }\n', conf,
                   problem1=(2, 9), problem2=(2, 17))
        self.check('---\n'
                   'dict: {   a: 1, b   }\n', conf)

    def test_max_spaces(self):
        conf = ('braces:\n'
                '  max-spaces-inside: 0\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'dict: {}\n', conf)
        self.check('---\n'
                   'dict: { }\n', conf, problem=(2, 8))
        self.check('---\n'
                   'dict: {a: 1, b}\n', conf)
        self.check('---\n'
                   'dict: { a: 1, b }\n', conf,
                   problem1=(2, 8), problem2=(2, 16))
        self.check('---\n'
                   'dict: {   a: 1, b   }\n', conf,
                   problem1=(2, 10), problem2=(2, 20))
        self.check('---\n'
                   'dict: {\n'
                   '  a: 1,\n'
                   '  b\n'
                   '}\n', conf)

        conf = ('braces:\n'
                '  max-spaces-inside: 3\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'dict: {   a: 1, b   }\n', conf)
        self.check('---\n'
                   'dict: {    a: 1, b     }\n', conf,
                   problem1=(2, 11), problem2=(2, 23))

    def test_min_and_max_spaces(self):
        conf = ('braces:\n'
                '  max-spaces-inside: 0\n'
                '  min-spaces-inside: 0\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'dict: {}\n', conf)
        self.check('---\n'
                   'dict: { }\n', conf, problem=(2, 8))
        self.check('---\n'
                   'dict: {   a: 1, b}\n', conf, problem=(2, 10))

        conf = ('braces:\n'
                '  max-spaces-inside: 1\n'
                '  min-spaces-inside: 1\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'dict: {a: 1, b, c: 3 }\n', conf, problem=(2, 8))

        conf = ('braces:\n'
                '  max-spaces-inside: 2\n'
                '  min-spaces-inside: 0\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'dict: {a: 1, b, c: 3 }\n', conf)
        self.check('---\n'
                   'dict: {  a: 1, b, c: 3 }\n', conf)
        self.check('---\n'
                   'dict: {   a: 1, b, c: 3 }\n', conf, problem=(2, 10))

    def test_min_spaces_empty(self):
        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: 0\n'
                '  min-spaces-inside-empty: 0\n')
        self.check('---\n'
                   'array: {}\n', conf)

        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: 1\n')
        self.check('---\n'
                   'array: {}\n', conf, problem=(2, 9))
        self.check('---\n'
                   'array: { }\n', conf)

        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: -1\n'
                '  min-spaces-inside-empty: 3\n')
        self.check('---\n'
                   'array: {}\n', conf, problem=(2, 9))
        self.check('---\n'
                   'array: {   }\n', conf)

    def test_max_spaces_empty(self):
        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: 0\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'array: {}\n', conf)
        self.check('---\n'
                   'array: { }\n', conf, problem=(2, 9))

        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: 1\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'array: {}\n', conf)
        self.check('---\n'
                   'array: { }\n', conf)
        self.check('---\n'
                   'array: {  }\n', conf, problem=(2, 10))

        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: 3\n'
                '  min-spaces-inside-empty: -1\n')
        self.check('---\n'
                   'array: {}\n', conf)
        self.check('---\n'
                   'array: {   }\n', conf)
        self.check('---\n'
                   'array: {    }\n', conf, problem=(2, 12))

    def test_min_and_max_spaces_empty(self):
        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: 2\n'
                '  min-spaces-inside-empty: 1\n')
        self.check('---\n'
                   'array: {}\n', conf, problem=(2, 9))
        self.check('---\n'
                   'array: { }\n', conf)
        self.check('---\n'
                   'array: {  }\n', conf)
        self.check('---\n'
                   'array: {   }\n', conf, problem=(2, 11))

    def test_mixed_empty_nonempty(self):
        conf = ('braces:\n'
                '  max-spaces-inside: -1\n'
                '  min-spaces-inside: 1\n'
                '  max-spaces-inside-empty: 0\n'
                '  min-spaces-inside-empty: 0\n')
        self.check('---\n'
                   'array: { a: 1, b }\n', conf)
        self.check('---\n'
                   'array: {a: 1, b}\n', conf,
                   problem1=(2, 9), problem2=(2, 16))
        self.check('---\n'
                   'array: {}\n', conf)
        self.check('---\n'
                   'array: { }\n', conf,
                   problem1=(2, 9))

        conf = ('braces:\n'
                '  max-spaces-inside: 0\n'
                '  min-spaces-inside: -1\n'
                '  max-spaces-inside-empty: 1\n'
                '  min-spaces-inside-empty: 1\n')
        self.check('---\n'
                   'array: { a: 1, b }\n', conf,
                   problem1=(2, 9), problem2=(2, 17))
        self.check('---\n'
                   'array: {a: 1, b}\n', conf)
        self.check('---\n'
                   'array: {}\n', conf,
                   problem1=(2, 9))
        self.check('---\n'
                   'array: { }\n', conf)

        conf = ('braces:\n'
                '  max-spaces-inside: 2\n'
                '  min-spaces-inside: 1\n'
                '  max-spaces-inside-empty: 1\n'
                '  min-spaces-inside-empty: 1\n')
        self.check('---\n'
                   'array: { a: 1, b  }\n', conf)
        self.check('---\n'
                   'array: {a: 1, b   }\n', conf,
                   problem1=(2, 9), problem2=(2, 18))
        self.check('---\n'
                   'array: {}\n', conf,
                   problem1=(2, 9))
        self.check('---\n'
                   'array: { }\n', conf)
        self.check('---\n'
                   'array: {   }\n', conf,
                   problem1=(2, 11))

        conf = ('braces:\n'
                '  max-spaces-inside: 1\n'
                '  min-spaces-inside: 1\n'
                '  max-spaces-inside-empty: 1\n'
                '  min-spaces-inside-empty: 1\n')
        self.check('---\n'
                   'array: { a: 1, b }\n', conf)
        self.check('---\n'
                   'array: {a: 1, b}\n', conf,
                   problem1=(2, 9), problem2=(2, 16))
        self.check('---\n'
                   'array: {}\n', conf,
                   problem1=(2, 9))
        self.check('---\n'
                   'array: { }\n', conf)
