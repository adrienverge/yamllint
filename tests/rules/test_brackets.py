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
    rule_id = 'brackets'

    def test_disabled(self):
        conf = 'brackets: disable'
        self.check('---\n'
                   'array1: []\n'
                   'array2: [ ]\n'
                   'array3: [   a, b]\n'
                   'array4: [a, b, c ]\n'
                   'array5: [a, b, c ]\n'
                   'array6: [  a, b, c ]\n'
                   'array7: [   a, b, c ]\n', conf)

    def test_min_spaces(self):
        conf = 'brackets: {max-spaces-inside: -1, min-spaces-inside: 0}'
        self.check('---\n'
                   'array: []\n', conf)

        conf = 'brackets: {max-spaces-inside: -1, min-spaces-inside: 1}'
        self.check('---\n'
                   'array: []\n', conf, problem=(2, 9))
        self.check('---\n'
                   'array: [ ]\n', conf)
        self.check('---\n'
                   'array: [a, b]\n', conf, problem1=(2, 9), problem2=(2, 13))
        self.check('---\n'
                   'array: [ a, b ]\n', conf)
        self.check('---\n'
                   'array: [\n'
                   '  a,\n'
                   '  b\n'
                   ']\n', conf)

        conf = 'brackets: {max-spaces-inside: -1, min-spaces-inside: 3}'
        self.check('---\n'
                   'array: [ a, b ]\n', conf,
                   problem1=(2, 10), problem2=(2, 15))
        self.check('---\n'
                   'array: [   a, b   ]\n', conf)

    def test_max_spaces(self):
        conf = 'brackets: {max-spaces-inside: 0, min-spaces-inside: -1}'
        self.check('---\n'
                   'array: []\n', conf)
        self.check('---\n'
                   'array: [ ]\n', conf, problem=(2, 9))
        self.check('---\n'
                   'array: [a, b]\n', conf)
        self.check('---\n'
                   'array: [ a, b ]\n', conf,
                   problem1=(2, 9), problem2=(2, 14))
        self.check('---\n'
                   'array: [   a, b   ]\n', conf,
                   problem1=(2, 11), problem2=(2, 18))
        self.check('---\n'
                   'array: [\n'
                   '  a,\n'
                   '  b\n'
                   ']\n', conf)

        conf = 'brackets: {max-spaces-inside: 3, min-spaces-inside: -1}'
        self.check('---\n'
                   'array: [   a, b   ]\n', conf)
        self.check('---\n'
                   'array: [    a, b     ]\n', conf,
                   problem1=(2, 12), problem2=(2, 21))

    def test_min_and_max_spaces(self):
        conf = 'brackets: {max-spaces-inside: 0, min-spaces-inside: 0}'
        self.check('---\n'
                   'array: []\n', conf)
        self.check('---\n'
                   'array: [ ]\n', conf, problem=(2, 9))
        self.check('---\n'
                   'array: [   a, b]\n', conf, problem=(2, 11))

        conf = 'brackets: {max-spaces-inside: 1, min-spaces-inside: 1}'
        self.check('---\n'
                   'array: [a, b, c ]\n', conf, problem=(2, 9))

        conf = 'brackets: {max-spaces-inside: 2, min-spaces-inside: 0}'
        self.check('---\n'
                   'array: [a, b, c ]\n', conf)
        self.check('---\n'
                   'array: [  a, b, c ]\n', conf)
        self.check('---\n'
                   'array: [   a, b, c ]\n', conf, problem=(2, 11))
