# -*- coding: utf-8 -*-
# Copyright (C) 2016 Peter Ericson
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


class TruthyTestCase(RuleTestCase):
    rule_id = 'truthy'

    def test_disabled(self):
        conf = 'truthy: disable'
        self.check('---\n'
                   '1: True\n', conf)
        self.check('---\n'
                   'True: 1\n', conf)

    def test_enabled(self):
        conf = 'truthy: enable\n'
        self.check('---\n'
                   '1: True\n', conf, problem=(2, 4))
        self.check('---\n'
                   'True: 1\n', conf, problem=(2, 1))
        self.check('---\n'
                   '1: "True"\n', conf)
        self.check('---\n'
                   '"True": 1\n', conf)

