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

from tests.rules.common import RuleTestCase


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
        conf = 'indentation: {spaces: 1}'
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
        conf = 'indentation: {spaces: 2}'
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
        conf = 'indentation: {spaces: 3}'
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

    def test_under_indented(self):
        conf = 'indentation: {spaces: 2}'
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
        conf = 'indentation: {spaces: 4}'
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

    def test_over_indented(self):
        conf = 'indentation: {spaces: 2}'
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
        conf = 'indentation: {spaces: 4}'
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
                   '    - subel\n'
                   '...\n', conf,
                   problem=(2, 3))
        self.check('---\n'
                   'object:\n'
                   '    k3:\n'
                   '        - name: Linux\n'
                   '           date: 1991\n'
                   '...\n', conf, problem=(5, 16, 'syntax'))

    def test_multi_lines(self):
        self.check('---\n'
                   'long_string: >\n'
                   '  bla bla blah\n'
                   '  blah bla bla\n'
                   '...\n', None)
        self.check('---\n'
                   '- long_string: >\n'
                   '    bla bla blah\n'
                   '    blah bla bla\n'
                   '...\n', None)
        self.check('---\n'
                   'obj:\n'
                   '  - long_string: >\n'
                   '      bla bla blah\n'
                   '      blah bla bla\n'
                   '...\n', None)

    def test_empty_value(self):
        conf = 'indentation: {spaces: 2}'
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

    def test_return(self):
        self.check('---\n'
                   'a:\n'
                   '  b:\n'
                   '    c:\n'
                   '  d:\n'
                   '    e:\n'
                   '      f:\n'
                   'g:\n'
                   '...\n', None)
        self.check('---\n'
                   'a:\n'
                   '  b:\n'
                   '    c:\n'
                   '   d:\n'
                   '...\n', None, problem=(5, 4, 'syntax'))
        self.check('---\n'
                   'a:\n'
                   '  b:\n'
                   '    c:\n'
                   ' d:\n'
                   '...\n', None, problem=(5, 2, 'syntax'))

    def test_first_line(self):
        conf = ('indentation: {spaces: 2}\n'
                'document-start: disable\n')
        self.check('  a: 1\n', conf, problem=(1, 3))

    def test_broken_inline_flows(self):
        conf = 'indentation: {spaces: 2}'
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
