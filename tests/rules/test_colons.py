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
    rule_id = 'colons'

    def test_disabled(self):
        conf = 'colons: disable'
        self.check('---\n'
                   'object:\n'
                   '  k1 : v1\n'
                   'obj2:\n'
                   '  k2     :\n'
                   '    - 8\n'
                   '  k3:\n'
                   '    val\n'
                   '  property   : value\n'
                   '  prop2      : val2\n'
                   '  propriété  : [valeur]\n'
                   '  o:\n'
                   '    k1: [v1, v2]\n'
                   '  p:\n'
                   '    - k3: >\n'
                   '        val\n'
                   '    - o: {k1: v1}\n'
                   '    - p: kdjf\n'
                   '    - q: val0\n'
                   '    - q2:\n'
                   '        - val1\n'
                   '...\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  k1:   v1\n'
                   'obj2:\n'
                   '  k2:\n'
                   '    - 8\n'
                   '  k3:\n'
                   '    val\n'
                   '  property:     value\n'
                   '  prop2:        val2\n'
                   '  propriété:    [valeur]\n'
                   '  o:\n'
                   '    k1:  [v1, v2]\n', conf)
        self.check('---\n'
                   'obj:\n'
                   '  p:\n'
                   '    - k1: >\n'
                   '        val\n'
                   '    - k3:  >\n'
                   '        val\n'
                   '    - o: {k1: v1}\n'
                   '    - o:  {k1: v1}\n'
                   '    - q2:\n'
                   '        - val1\n'
                   '...\n', conf)
        self.check('---\n'
                   'a: {b: {c:  d, e : f}}\n', conf)

    def test_before_enabled(self):
        conf = 'colons: {max-spaces-before: 0, max-spaces-after: -1}'
        self.check('---\n'
                   'object:\n'
                   '  k1:\n'
                   '    - a\n'
                   '    - b\n'
                   '  k2: v2\n'
                   '...\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  k1 :\n'
                   '    - a\n'
                   '    - b\n'
                   '  k2: v2\n'
                   '...\n', conf, problem=(3, 5))
        self.check('---\n'
                   'lib :\n'
                   '  - var\n'
                   '...\n', conf, problem=(2, 4))
        self.check('---\n'
                   '- lib :\n'
                   '    - var\n'
                   '...\n', conf, problem=(2, 6))
        self.check('---\n'
                   'a: {b: {c : d, e : f}}\n', conf,
                   problem1=(2, 10), problem2=(2, 17))

    def test_before_max(self):
        conf = 'colons: {max-spaces-before: 3, max-spaces-after: -1}'
        self.check('---\n'
                   'object :\n'
                   '  k1   :\n'
                   '    - a\n'
                   '    - b\n'
                   '  k2  : v2\n'
                   '...\n', conf)
        self.check('---\n'
                   'object :\n'
                   '  k1    :\n'
                   '    - a\n'
                   '    - b\n'
                   '  k2  : v2\n'
                   '...\n', conf, problem=(3, 8))

    def test_before_with_explicit_block_mappings(self):
        conf = 'colons: {max-spaces-before: 0, max-spaces-after: 1}'
        self.check('---\n'
                   'object:\n'
                   '  ? key\n'
                   '  : value\n'
                   '...\n', conf)
        self.check('---\n'
                   'object :\n'
                   '  ? key\n'
                   '  : value\n'
                   '...\n', conf, problem=(2, 7))
        self.check('---\n'
                   '? >\n'
                   '    multi-line\n'
                   '    key\n'
                   ': >\n'
                   '    multi-line\n'
                   '    value\n'
                   '...\n', conf)
        self.check('---\n'
                   '- ? >\n'
                   '      multi-line\n'
                   '      key\n'
                   '  : >\n'
                   '      multi-line\n'
                   '      value\n'
                   '...\n', conf)
        self.check('---\n'
                   '- ? >\n'
                   '      multi-line\n'
                   '      key\n'
                   '  :  >\n'
                   '       multi-line\n'
                   '       value\n'
                   '...\n', conf, problem=(5, 5))

    def test_after_enabled(self):
        conf = 'colons: {max-spaces-before: -1, max-spaces-after: 1}'
        self.check('---\n'
                   'key: value\n', conf)
        self.check('---\n'
                   'key:  value\n', conf, problem=(2, 6))
        self.check('---\n'
                   'object:\n'
                   '  k1:  [a, b]\n'
                   '  k2: string\n', conf, problem=(3, 7))
        self.check('---\n'
                   'object:\n'
                   '  k1: [a, b]\n'
                   '  k2:  string\n', conf, problem=(4, 7))
        self.check('---\n'
                   'object:\n'
                   '  other: {key:  value}\n'
                   '...\n', conf, problem=(3, 16))
        self.check('---\n'
                   'a: {b: {c:  d, e :  f}}\n', conf,
                   problem1=(2, 12), problem2=(2, 20))

    def test_after_enabled_question_mark(self):
        conf = 'colons: {max-spaces-before: -1, max-spaces-after: 1}'
        self.check('---\n'
                   '? key\n'
                   ': value\n', conf)
        self.check('---\n'
                   '?  key\n'
                   ': value\n', conf, problem=(2, 3))
        self.check('---\n'
                   '?  key\n'
                   ':  value\n', conf, problem1=(2, 3), problem2=(3, 3))
        self.check('---\n'
                   '- ?  key\n'
                   '  :  value\n', conf, problem1=(2, 5), problem2=(3, 5))

    def test_after_max(self):
        conf = 'colons: {max-spaces-before: -1, max-spaces-after: 3}'
        self.check('---\n'
                   'object:\n'
                   '  k1:  [a, b]\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  k1:    [a, b]\n', conf, problem=(3, 9))
        self.check('---\n'
                   'object:\n'
                   '  k2:  string\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  k2:    string\n', conf, problem=(3, 9))
        self.check('---\n'
                   'object:\n'
                   '  other: {key:  value}\n'
                   '...\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  other: {key:    value}\n'
                   '...\n', conf, problem=(3, 18))

    def test_after_with_explicit_block_mappings(self):
        conf = 'colons: {max-spaces-before: -1, max-spaces-after: 1}'
        self.check('---\n'
                   'object:\n'
                   '  ? key\n'
                   '  : value\n'
                   '...\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  ? key\n'
                   '  :  value\n'
                   '...\n', conf, problem=(4, 5))

    def test_after_do_not_confound_with_trailing_space(self):
        conf = ('colons: {max-spaces-before: 1, max-spaces-after: 1}\n'
                'trailing-spaces: disable\n')
        self.check('---\n'
                   'trailing:     \n'
                   '  - spaces\n', conf)

    def test_both_before_and_after(self):
        conf = 'colons: {max-spaces-before: 0, max-spaces-after: 1}'
        self.check('---\n'
                   'obj:\n'
                   '  string: text\n'
                   '  k:\n'
                   '    - 8\n'
                   '  k3:\n'
                   '    val\n'
                   '  property: [value]\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  k1 :  v1\n', conf, problem1=(3, 5), problem2=(3, 8))
        self.check('---\n'
                   'obj:\n'
                   '  string:  text\n'
                   '  k :\n'
                   '    - 8\n'
                   '  k3:\n'
                   '    val\n'
                   '  property: {a: 1, b:  2, c : 3}\n', conf,
                   problem1=(3, 11), problem2=(4, 4),
                   problem3=(8, 23), problem4=(8, 28))
