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

    def test_disabled_globally(self):
        conf = 'empty-values: disable'
        self.check('---\n'
                   'foo:\n', conf)

        self.check('---\n'
                   'foo:\n'
                   ' bar:\n', conf)

    def test_disabled_forbid_in_block_mappings(self):
        conf = 'empty-values: {forbid-in-block-mappings: false}'
        self.check('---\n'
                   'foo:\n', conf)

        self.check('---\n'
                   'foo:\n'
                   'bar: aaa\n', conf)

    def test_single_line(self):
        conf = 'empty-values: {forbid-in-block-mappings: true}\n'
        self.check('---\n'
                   'implicitly-null:\n', conf, problem1=(2, 17))

        self.check('---\n'
                   'implicitly-null:with-colons:in-key:\n', conf,
                   problem1=(2, 36))

        self.check('---\n'
                   'implicitly-null:with-colons:in-key2:\n', conf,
                   problem1=(2, 37))

    def test_enabled_all_lines(self):
        conf = 'empty-values: {forbid-in-block-mappings: true}\n'
        self.check('---\n'
                   'foo:\n'
                   'bar:\n'
                   'foobar:\n', conf, problem1=(2, 5),
                   problem2=(3, 5), problem3=(4, 8))

    def test_enabled_explicit_end_of_document(self):
        conf = 'empty-values: {forbid-in-block-mappings: true}\n'
        self.check('---\n'
                   'foo:\n'
                   '...\n', conf, problem1=(2, 5))

    def test_enabled_not_end_of_document(self):
        conf = 'empty-values: {forbid-in-block-mappings: true}\n'
        self.check('---\n'
                   'foo:\n'
                   'bar:\n'
                   ' aaa\n', conf, problem1=(2, 5))

    def test_enabled_different_level(self):
        conf = 'empty-values: {forbid-in-block-mappings: true}\n'
        self.check('---\n'
                   'foo:\n'
                   ' bar:\n'
                   'aaa: bbb\n', conf, problem1=(3, 6))

    def test_enabled_empty_flow_mapping(self):
        conf = 'empty-values: {forbid-in-block-mappings: true}\n'
        self.check('---\n'
                   'foo: {a:}\n', conf)

    def test_enabled_empty_block_sequence(self):
        conf = 'empty-values: {forbid-in-block-mappings: true}\n'
        self.check('---\n'
                   'foo:\n'
                   '  -\n', conf)

    def test_enabled_not_empty_or_explicit_null(self):
        conf = 'empty-values: {forbid-in-block-mappings: true}\n'
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

    def test_enabled_various_explicit_null(self):
        conf = 'empty-values: {forbid-in-block-mappings: true}\n'
        self.check('---\n'
                   'null-key1: {?: val}\n', conf)

        self.check('---\n'
                   'null-alias: ~\n', conf)

        self.check('---\n'
                   'null-key2: {? !!null "": val}\n', conf)
