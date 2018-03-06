# -*- coding: utf-8 -*-
# Copyright (C) 2017 Greg Dubicki
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


class EmptyValuesTestCase(RuleTestCase):
    rule_id = 'empty-values'

    def test_disabled(self):
        conf = ('empty-values: disable\n'
                'braces: disable\n'
                'commas: disable\n')
        self.check('---\n'
                   'foo:\n', conf)
        self.check('---\n'
                   'foo:\n'
                   ' bar:\n', conf)
        self.check('---\n'
                   '{a:}\n', conf)
        self.check('---\n'
                   'foo: {a:}\n', conf)
        self.check('---\n'
                   '- {a:}\n'
                   '- {a:, b: 2}\n'
                   '- {a: 1, b:}\n'
                   '- {a: 1, b: , }\n', conf)
        self.check('---\n'
                   '{a: {b: , c: {d: 4, e:}}, f:}\n', conf)

    def test_in_block_mappings_disabled(self):
        conf = ('empty-values: {forbid-in-block-mappings: false,\n'
                '               forbid-in-flow-mappings: false}\n')
        self.check('---\n'
                   'foo:\n', conf)
        self.check('---\n'
                   'foo:\n'
                   'bar: aaa\n', conf)

    def test_in_block_mappings_single_line(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n')
        self.check('---\n'
                   'implicitly-null:\n', conf, problem1=(2, 17))
        self.check('---\n'
                   'implicitly-null:with-colons:in-key:\n', conf,
                   problem1=(2, 36))
        self.check('---\n'
                   'implicitly-null:with-colons:in-key2:\n', conf,
                   problem1=(2, 37))

    def test_in_block_mappings_all_lines(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n')
        self.check('---\n'
                   'foo:\n'
                   'bar:\n'
                   'foobar:\n', conf, problem1=(2, 5),
                   problem2=(3, 5), problem3=(4, 8))

    def test_in_block_mappings_explicit_end_of_document(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n')
        self.check('---\n'
                   'foo:\n'
                   '...\n', conf, problem1=(2, 5))

    def test_in_block_mappings_not_end_of_document(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n')
        self.check('---\n'
                   'foo:\n'
                   'bar:\n'
                   ' aaa\n', conf, problem1=(2, 5))

    def test_in_block_mappings_different_level(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n')
        self.check('---\n'
                   'foo:\n'
                   ' bar:\n'
                   'aaa: bbb\n', conf, problem1=(3, 6))

    def test_in_block_mappings_empty_flow_mapping(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n'
                'braces: disable\n'
                'commas: disable\n')
        self.check('---\n'
                   'foo: {a:}\n', conf)
        self.check('---\n'
                   '- {a:, b: 2}\n'
                   '- {a: 1, b:}\n'
                   '- {a: 1, b: , }\n', conf)

    def test_in_block_mappings_empty_block_sequence(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n')
        self.check('---\n'
                   'foo:\n'
                   '  -\n', conf)

    def test_in_block_mappings_not_empty_or_explicit_null(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n')
        self.check('---\n'
                   'foo:\n'
                   ' bar:\n'
                   '  aaa\n', conf)
        self.check('---\n'
                   'explicitly-null: null\n', conf)
        self.check('---\n'
                   'explicitly-null:with-colons:in-key: null\n', conf)
        self.check('---\n'
                   'false-null: nulL\n', conf)
        self.check('---\n'
                   'empty-string: \'\'\n', conf)
        self.check('---\n'
                   'nullable-boolean: false\n', conf)
        self.check('---\n'
                   'nullable-int: 0\n', conf)
        self.check('---\n'
                   'First occurrence: &anchor Foo\n'
                   'Second occurrence: *anchor\n', conf)

    def test_in_block_mappings_various_explicit_null(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n')
        self.check('---\n'
                   'null-alias: ~\n', conf)
        self.check('---\n'
                   'null-key1: {?: val}\n', conf)
        self.check('---\n'
                   'null-key2: {? !!null "": val}\n', conf)

    def test_in_block_mappings_comments(self):
        conf = ('empty-values: {forbid-in-block-mappings: true,\n'
                '               forbid-in-flow-mappings: false}\n'
                'comments: disable\n')
        self.check('---\n'
                   'empty:  # comment\n'
                   'foo:\n'
                   '  bar: # comment\n', conf,
                   problem1=(2, 7),
                   problem2=(4, 7))

    def test_in_flow_mappings_disabled(self):
        conf = ('empty-values: {forbid-in-block-mappings: false,\n'
                '               forbid-in-flow-mappings: false}\n'
                'braces: disable\n'
                'commas: disable\n')
        self.check('---\n'
                   '{a:}\n', conf)
        self.check('---\n'
                   'foo: {a:}\n', conf)
        self.check('---\n'
                   '- {a:}\n'
                   '- {a:, b: 2}\n'
                   '- {a: 1, b:}\n'
                   '- {a: 1, b: , }\n', conf)
        self.check('---\n'
                   '{a: {b: , c: {d: 4, e:}}, f:}\n', conf)

    def test_in_flow_mappings_single_line(self):
        conf = ('empty-values: {forbid-in-block-mappings: false,\n'
                '               forbid-in-flow-mappings: true}\n'
                'braces: disable\n'
                'commas: disable\n')
        self.check('---\n'
                   '{a:}\n', conf,
                   problem=(2, 4))
        self.check('---\n'
                   'foo: {a:}\n', conf,
                   problem=(2, 9))
        self.check('---\n'
                   '- {a:}\n'
                   '- {a:, b: 2}\n'
                   '- {a: 1, b:}\n'
                   '- {a: 1, b: , }\n', conf,
                   problem1=(2, 6),
                   problem2=(3, 6),
                   problem3=(4, 12),
                   problem4=(5, 12))
        self.check('---\n'
                   '{a: {b: , c: {d: 4, e:}}, f:}\n', conf,
                   problem1=(2, 8),
                   problem2=(2, 23),
                   problem3=(2, 29))

    def test_in_flow_mappings_multi_line(self):
        conf = ('empty-values: {forbid-in-block-mappings: false,\n'
                '               forbid-in-flow-mappings: true}\n'
                'braces: disable\n'
                'commas: disable\n')
        self.check('---\n'
                   'foo: {\n'
                   '  a:\n'
                   '}\n', conf,
                   problem=(3, 5))
        self.check('---\n'
                   '{\n'
                   '  a: {\n'
                   '    b: ,\n'
                   '    c: {\n'
                   '      d: 4,\n'
                   '      e:\n'
                   '    }\n'
                   '  },\n'
                   '  f:\n'
                   '}\n', conf,
                   problem1=(4, 7),
                   problem2=(7, 9),
                   problem3=(10, 5))

    def test_in_flow_mappings_various_explicit_null(self):
        conf = ('empty-values: {forbid-in-block-mappings: false,\n'
                '               forbid-in-flow-mappings: true}\n'
                'braces: disable\n'
                'commas: disable\n')
        self.check('---\n'
                   '{explicit-null: null}\n', conf)
        self.check('---\n'
                   '{null-alias: ~}\n', conf)
        self.check('---\n'
                   'null-key1: {?: val}\n', conf)
        self.check('---\n'
                   'null-key2: {? !!null "": val}\n', conf)

    def test_in_flow_mappings_comments(self):
        conf = ('empty-values: {forbid-in-block-mappings: false,\n'
                '               forbid-in-flow-mappings: true}\n'
                'braces: disable\n'
                'commas: disable\n'
                'comments: disable\n')
        self.check('---\n'
                   '{\n'
                   '  a: {\n'
                   '    b: ,  # comment\n'
                   '    c: {\n'
                   '      d: 4,  # comment\n'
                   '      e:  # comment\n'
                   '    }\n'
                   '  },\n'
                   '  f:  # comment\n'
                   '}\n', conf,
                   problem1=(4, 7),
                   problem2=(7, 9),
                   problem3=(10, 5))
