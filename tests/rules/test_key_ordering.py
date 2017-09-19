# -*- coding: utf-8 -*-
# Copyright (C) 2017 Johannes F. Knauf
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


class KeyOrderingTestCase(RuleTestCase):
    rule_id = 'key-ordering'

    def test_disabled(self):
        conf = 'key-ordering: disable'
        self.check('---\n'
                   'block mapping:\n'
                   '  secondkey: a\n'
                   '  firstkey: b\n', conf)
        self.check('---\n'
                   'flow mapping:\n'
                   '  {secondkey: a, firstkey: b}\n', conf)
        self.check('---\n'
                   'second: before_first\n'
                   'at: root\n', conf)
        self.check('---\n'
                   'nested but OK:\n'
                   '  second: {first: 1}\n'
                   '  third:\n'
                   '    second: 2\n', conf)

    def test_enabled(self):
        conf = 'key-ordering: enable'
        self.check('---\n'
                   'block mapping:\n'
                   '  secondkey: a\n'
                   '  firstkey: b\n', conf,
                   problem=(4, 3))
        self.check('---\n'
                   'flow mapping:\n'
                   '  {secondkey: a, firstkey: b}\n', conf,
                   problem=(3, 18))
        self.check('---\n'
                   'second: before_first\n'
                   'at: root\n', conf,
                   problem=(3, 1))
        self.check('---\n'
                   'nested but OK:\n'
                   '  second: {first: 1}\n'
                   '  third:\n'
                   '    second: 2\n', conf)

    def test_key_tokens_in_flow_sequences(self):
        conf = 'key-ordering: enable'
        self.check('---\n'
                   '[\n'
                   '  key: value, mappings, in, flow: sequence\n'
                   ']\n', conf)
