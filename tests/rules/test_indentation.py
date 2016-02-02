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
        conf = 'indentation: {spaces: 1, indent-sequences: no}'
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
        conf = 'indentation: {spaces: 1, indent-sequences: yes}'
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
        conf = 'indentation: {spaces: 2, indent-sequences: no}'
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
        conf = 'indentation: {spaces: 2, indent-sequences: yes}'
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
        conf = 'indentation: {spaces: 3, indent-sequences: no}'
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
        conf = 'indentation: {spaces: 3, indent-sequences: yes}'
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

    def test_direct_flows(self):
        # flow: [ ...
        # ]
        conf = 'indentation: {spaces: 2}'
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
        conf = 'indentation: {spaces: 2}'
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
                   '}\n', conf, problem=(3, 4))
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
                   ']\n', conf, problem=(3, 4))
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

    def test_cleared_flows(self):
        # flow:
        #   [
        #     ...
        #   ]
        conf = 'indentation: {spaces: 2}'
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
                   '   ]\n', conf, problem=(3, 4))
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
        conf = 'indentation: {spaces: 2, indent-sequences: yes}'
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
        conf = 'indentation: {spaces: 4, indent-sequences: yes}'
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
        conf = 'indentation: {spaces: 2, indent-sequences: yes}'
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
        conf = 'indentation: {spaces: 4, indent-sequences: yes}'
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

    def test_multi_lines(self):
        conf = 'indentation: {spaces: 2, indent-sequences: yes}'
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
        conf = 'indentation: {spaces: 2}'
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
        conf = ('indentation: {spaces: 2}\n'
                'document-start: disable\n')
        self.check('  a: 1\n', conf, problem=(1, 3))

    def test_explicit_block_mappings(self):
        conf = 'indentation: {spaces: 4}'
        self.check('---\n'
                   'object:\n'
                   '    ? key\n'
                   '    :\n'
                   '        value\n'
                   '...\n', conf)
        self.check('---\n'
                   'object:\n'
                   '    ? key\n'
                   '    :\n'
                   '       value\n'
                   '...\n', conf, problem=(5, 8))
        self.check('---\n'
                   'object:\n'
                   '    ?\n'
                   '        key\n'
                   '    :\n'
                   '        value\n'
                   '...\n', conf)
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
        conf = 'indentation: {spaces: 2}'
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
        self.check('---\n'
                   '-\n'
                   '  -\n'
                   '     >\n'
                   '      multi\n'
                   '      line\n'
                   '...\n', conf, problem=(4, 6))


class ScalarIndentationTestCase(RuleTestCase):
    rule_id = 'indentation'

    def test_basics_plain(self):
        conf = ('indentation: {spaces: 2, check-multi-line-strings: no}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: yes}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: no}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: yes}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: no}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: yes}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: no}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: yes}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: yes}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: yes}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: yes}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: yes}\n'
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
        conf = ('indentation: {spaces: 2, check-multi-line-strings: yes}\n'
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
