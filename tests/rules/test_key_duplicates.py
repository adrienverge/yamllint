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


class KeyDuplicatesTestCase(RuleTestCase):
    rule_id = 'key-duplicates'

    def test_disabled(self):
        conf = 'key-duplicates: disable'
        self.check('---\n'
                   'block mapping:\n'
                   '  key: a\n'
                   '  otherkey: b\n'
                   '  key: c\n', conf)
        self.check('---\n'
                   'flow mapping:\n'
                   '  {key: a, otherkey: b, key: c}\n', conf)
        self.check('---\n'
                   'duplicated twice:\n'
                   '  - k: a\n'
                   '    ok: b\n'
                   '    k: c\n'
                   '    k: d\n', conf)
        self.check('---\n'
                   'duplicated twice:\n'
                   '  - {k: a, ok: b, k: c, k: d}\n', conf)
        self.check('---\n'
                   'multiple duplicates:\n'
                   '  a: 1\n'
                   '  b: 2\n'
                   '  c: 3\n'
                   '  d: 4\n'
                   '  d: 5\n'
                   '  b: 6\n', conf)
        self.check('---\n'
                   'multiple duplicates:\n'
                   '  {a: 1, b: 2, c: 3, d: 4, d: 5, b: 6}\n', conf)
        self.check('---\n'
                   'at: root\n'
                   'multiple: times\n'
                   'at: root\n', conf)
        self.check('---\n'
                   'nested but OK:\n'
                   '  a: {a: {a: 1}}\n'
                   '  b:\n'
                   '    b: 2\n'
                   '    c: 3\n', conf)
        self.check('---\n'
                   'nested duplicates:\n'
                   '  a: {a: 1, a: 1}\n'
                   '  b:\n'
                   '    c: 3\n'
                   '    d: 4\n'
                   '    d: 4\n'
                   '  b: 2\n', conf)
        self.check('---\n'
                   'duplicates with many styles: 1\n'
                   '"duplicates with many styles": 1\n'
                   '\'duplicates with many styles\': 1\n'
                   '? duplicates with many styles\n'
                   ': 1\n'
                   '? >-\n'
                   '    duplicates with\n'
                   '    many styles\n'
                   ': 1\n', conf)
        self.check('---\n'
                   'Merge Keys are OK:\n'
                   'anchor_one: &anchor_one\n'
                   '  one: one\n'
                   'anchor_two: &anchor_two\n'
                   '  two: two\n'
                   'anchor_reference:\n'
                   '  <<: *anchor_one\n'
                   '  <<: *anchor_two\n', conf)

    def test_enabled(self):
        conf = 'key-duplicates: enable'
        self.check('---\n'
                   'block mapping:\n'
                   '  key: a\n'
                   '  otherkey: b\n'
                   '  key: c\n', conf,
                   problem=(5, 3))
        self.check('---\n'
                   'flow mapping:\n'
                   '  {key: a, otherkey: b, key: c}\n', conf,
                   problem=(3, 25))
        self.check('---\n'
                   'duplicated twice:\n'
                   '  - k: a\n'
                   '    ok: b\n'
                   '    k: c\n'
                   '    k: d\n', conf,
                   problem1=(5, 5), problem2=(6, 5))
        self.check('---\n'
                   'duplicated twice:\n'
                   '  - {k: a, ok: b, k: c, k: d}\n', conf,
                   problem1=(3, 19), problem2=(3, 25))
        self.check('---\n'
                   'multiple duplicates:\n'
                   '  a: 1\n'
                   '  b: 2\n'
                   '  c: 3\n'
                   '  d: 4\n'
                   '  d: 5\n'
                   '  b: 6\n', conf,
                   problem1=(7, 3), problem2=(8, 3))
        self.check('---\n'
                   'multiple duplicates:\n'
                   '  {a: 1, b: 2, c: 3, d: 4, d: 5, b: 6}\n', conf,
                   problem1=(3, 28), problem2=(3, 34))
        self.check('---\n'
                   'at: root\n'
                   'multiple: times\n'
                   'at: root\n', conf,
                   problem=(4, 1))
        self.check('---\n'
                   'nested but OK:\n'
                   '  a: {a: {a: 1}}\n'
                   '  b:\n'
                   '    b: 2\n'
                   '    c: 3\n', conf)
        self.check('---\n'
                   'nested duplicates:\n'
                   '  a: {a: 1, a: 1}\n'
                   '  b:\n'
                   '    c: 3\n'
                   '    d: 4\n'
                   '    d: 4\n'
                   '  b: 2\n', conf,
                   problem1=(3, 13), problem2=(7, 5), problem3=(8, 3))
        self.check('---\n'
                   'duplicates with many styles: 1\n'
                   '"duplicates with many styles": 1\n'
                   '\'duplicates with many styles\': 1\n'
                   '? duplicates with many styles\n'
                   ': 1\n'
                   '? >-\n'
                   '    duplicates with\n'
                   '    many styles\n'
                   ': 1\n', conf,
                   problem1=(3, 1), problem2=(4, 1), problem3=(5, 3),
                   problem4=(7, 3))
        self.check('---\n'
                   'Merge Keys are OK:\n'
                   'anchor_one: &anchor_one\n'
                   '  one: one\n'
                   'anchor_two: &anchor_two\n'
                   '  two: two\n'
                   'anchor_reference:\n'
                   '  <<: *anchor_one\n'
                   '  <<: *anchor_two\n', conf)

    def test_key_tokens_in_flow_sequences(self):
        conf = 'key-duplicates: enable'
        self.check('---\n'
                   '[\n'
                   '  flow: sequence, with, key: value, mappings\n'
                   ']\n', conf)
