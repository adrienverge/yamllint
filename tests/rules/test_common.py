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

from yamllint.rules.common import get_line_indent


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
