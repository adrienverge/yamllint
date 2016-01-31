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


class CommaTestCase(RuleTestCase):
    rule_id = 'commas'

    def test_disabled(self):
        conf = 'commas: disable'
        self.check('---\n'
                   'dict: {a: b ,   c: "1 2 3",    d: e , f: [g,      h]}\n'
                   'array: [\n'
                   '  elem  ,\n'
                   '  key: val ,\n'
                   ']\n'
                   'map: {\n'
                   '  key1: val1 ,\n'
                   '  key2: val2,\n'
                   '}\n'
                   '...\n', conf)
        self.check('---\n'
                   '- [one, two , three,four]\n'
                   '- {five,six , seven, eight}\n'
                   '- [\n'
                   '  nine,  ten\n'
                   '  , eleven\n'
                   '  ,twelve\n'
                   ']\n'
                   '- {\n'
                   '  thirteen: 13,  fourteen\n'
                   '  , fifteen: 15\n'
                   '  ,sixteen: 16\n'
                   '}\n', conf)

    def test_before_max(self):
        conf = ('commas:\n'
                '  max-spaces-before: 0\n'
                '  min-spaces-after: 0\n'
                '  max-spaces-after: -1\n')
        self.check('---\n'
                   'array: [1, 2,  3, 4]\n'
                   '...\n', conf)
        self.check('---\n'
                   'array: [1, 2 ,  3, 4]\n'
                   '...\n', conf, problem=(2, 13))
        self.check('---\n'
                   'array: [1 , 2,  3      , 4]\n'
                   '...\n', conf, problem1=(2, 10), problem2=(2, 23))
        self.check('---\n'
                   'dict: {a: b, c: "1 2 3", d: e,  f: [g, h]}\n'
                   '...\n', conf)
        self.check('---\n'
                   'dict: {a: b, c: "1 2 3" , d: e,  f: [g, h]}\n'
                   '...\n', conf, problem=(2, 24))
        self.check('---\n'
                   'dict: {a: b , c: "1 2 3", d: e,  f: [g    , h]}\n'
                   '...\n', conf, problem1=(2, 12), problem2=(2, 42))
        self.check('---\n'
                   'array: [\n'
                   '  elem,\n'
                   '  key: val,\n'
                   ']\n', conf)
        self.check('---\n'
                   'array: [\n'
                   '  elem ,\n'
                   '  key: val,\n'
                   ']\n', conf, problem=(3, 7))
        self.check('---\n'
                   'map: {\n'
                   '  key1: val1,\n'
                   '  key2: val2,\n'
                   '}\n', conf)
        self.check('---\n'
                   'map: {\n'
                   '  key1: val1,\n'
                   '  key2: val2 ,\n'
                   '}\n', conf, problem=(4, 13))

    def test_before_max_with_comma_on_new_line(self):
        conf = ('commas:\n'
                '  max-spaces-before: 0\n'
                '  min-spaces-after: 0\n'
                '  max-spaces-after: -1\n')
        self.check('---\n'
                   'flow-seq: [1, 2, 3\n'
                   '           , 4, 5, 6]\n'
                   '...\n', conf, problem=(3, 11))
        self.check('---\n'
                   'flow-map: {a: 1, b: 2\n'
                   '           , c: 3}\n'
                   '...\n', conf, problem=(3, 11))

        conf = ('commas:\n'
                '  max-spaces-before: 0\n'
                '  min-spaces-after: 0\n'
                '  max-spaces-after: -1\n'
                'indentation: disable\n')
        self.check('---\n'
                   'flow-seq: [1, 2, 3\n'
                   '         , 4, 5, 6]\n'
                   '...\n', conf, problem=(3, 9))
        self.check('---\n'
                   'flow-map: {a: 1, b: 2\n'
                   '         , c: 3}\n'
                   '...\n', conf, problem=(3, 9))
        self.check('---\n'
                   '[\n'
                   '1,\n'
                   '2\n'
                   ', 3\n'
                   ']\n', conf, problem=(5, 1))
        self.check('---\n'
                   '{\n'
                   'a: 1,\n'
                   'b: 2\n'
                   ', c: 3\n'
                   '}\n', conf, problem=(5, 1))

    def test_before_max_3(self):
        conf = ('commas:\n'
                '  max-spaces-before: 3\n'
                '  min-spaces-after: 0\n'
                '  max-spaces-after: -1\n')
        self.check('---\n'
                   'array: [1 , 2, 3   , 4]\n'
                   '...\n', conf)
        self.check('---\n'
                   'array: [1 , 2, 3    , 4]\n'
                   '...\n', conf, problem=(2, 20))
        self.check('---\n'
                   'array: [\n'
                   '  elem1   ,\n'
                   '  elem2    ,\n'
                   '  key: val,\n'
                   ']\n', conf, problem=(4, 11))

    def test_after_min(self):
        conf = ('commas:\n'
                '  max-spaces-before: -1\n'
                '  min-spaces-after: 1\n'
                '  max-spaces-after: -1\n')
        self.check('---\n'
                   '- [one, two , three,four]\n'
                   '- {five,six , seven, eight}\n'
                   '- [\n'
                   '  nine,  ten\n'
                   '  , eleven\n'
                   '  ,twelve\n'
                   ']\n'
                   '- {\n'
                   '  thirteen: 13,  fourteen\n'
                   '  , fifteen: 15\n'
                   '  ,sixteen: 16\n'
                   '}\n', conf,
                   problem1=(2, 21), problem2=(3, 9),
                   problem3=(7, 4), problem4=(12, 4))

    def test_after_max(self):
        conf = ('commas:\n'
                '  max-spaces-before: -1\n'
                '  min-spaces-after: 0\n'
                '  max-spaces-after: 1\n')
        self.check('---\n'
                   'array: [1, 2, 3, 4]\n'
                   '...\n', conf)
        self.check('---\n'
                   'array: [1, 2,  3, 4]\n'
                   '...\n', conf, problem=(2, 15))
        self.check('---\n'
                   'array: [1,  2, 3,     4]\n'
                   '...\n', conf, problem1=(2, 12), problem2=(2, 22))
        self.check('---\n'
                   'dict: {a: b , c: "1 2 3", d: e, f: [g, h]}\n'
                   '...\n', conf)
        self.check('---\n'
                   'dict: {a: b , c: "1 2 3",  d: e, f: [g, h]}\n'
                   '...\n', conf, problem=(2, 27))
        self.check('---\n'
                   'dict: {a: b ,  c: "1 2 3", d: e, f: [g,     h]}\n'
                   '...\n', conf, problem1=(2, 15), problem2=(2, 44))
        self.check('---\n'
                   'array: [\n'
                   '  elem,\n'
                   '  key: val,\n'
                   ']\n', conf)
        self.check('---\n'
                   'array: [\n'
                   '  elem,  key: val,\n'
                   ']\n', conf, problem=(3, 9))
        self.check('---\n'
                   'map: {\n'
                   '  key1: val1,   key2: [val2,  val3]\n'
                   '}\n', conf, problem1=(3, 16), problem2=(3, 30))

    def test_after_max_3(self):
        conf = ('commas:\n'
                '  max-spaces-before: -1\n'
                '  min-spaces-after: 1\n'
                '  max-spaces-after: 3\n')
        self.check('---\n'
                   'array: [1,  2, 3,   4]\n'
                   '...\n', conf)
        self.check('---\n'
                   'array: [1,  2, 3,    4]\n'
                   '...\n', conf, problem=(2, 21))
        self.check('---\n'
                   'dict: {a: b ,   c: "1 2 3",    d: e, f: [g,      h]}\n'
                   '...\n', conf, problem1=(2, 31), problem2=(2, 49))

    def test_both_before_and_after(self):
        conf = ('commas:\n'
                '  max-spaces-before: 0\n'
                '  min-spaces-after: 1\n'
                '  max-spaces-after: 1\n')
        self.check('---\n'
                   'dict: {a: b ,   c: "1 2 3",    d: e , f: [g,      h]}\n'
                   'array: [\n'
                   '  elem  ,\n'
                   '  key: val ,\n'
                   ']\n'
                   'map: {\n'
                   '  key1: val1 ,\n'
                   '  key2: val2,\n'
                   '}\n'
                   '...\n', conf,
                   problem1=(2, 12), problem2=(2, 16), problem3=(2, 31),
                   problem4=(2, 36), problem5=(2, 50), problem6=(4, 8),
                   problem7=(5, 11), problem8=(8, 13))
        conf = ('commas:\n'
                '  max-spaces-before: 0\n'
                '  min-spaces-after: 1\n'
                '  max-spaces-after: 1\n'
                'indentation: disable\n')
        self.check('---\n'
                   '- [one, two , three,four]\n'
                   '- {five,six , seven, eight}\n'
                   '- [\n'
                   '  nine,  ten\n'
                   '  , eleven\n'
                   '  ,twelve\n'
                   ']\n'
                   '- {\n'
                   '  thirteen: 13,  fourteen\n'
                   '  , fifteen: 15\n'
                   '  ,sixteen: 16\n'
                   '}\n', conf,
                   problem1=(2, 12), problem2=(2, 21), problem3=(3, 9),
                   problem4=(3, 12), problem5=(5, 9), problem6=(6, 2),
                   problem7=(7, 2), problem8=(7, 4), problem9=(10, 17),
                   problem10=(11, 2), problem11=(12, 2), problem12=(12, 4))
