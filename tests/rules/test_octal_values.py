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


class OctalValuesTestCase(RuleTestCase):
    rule_id = 'octal-values'

    def test_disabled(self):
        conf = ('octal-values: disable\n'
                'new-line-at-end-of-file: disable\n'
                'document-start: disable\n')
        self.check('user-city: 010', conf)
        self.check('user-city: 0o10', conf)

    def test_implicit_octal_values(self):
        conf = ('octal-values:\n'
                '  forbid-implicit-octal: true\n'
                '  forbid-explicit-octal: false\n'
                'new-line-at-end-of-file: disable\n'
                'document-start: disable\n')
        self.check('user-city: 010', conf, problem=(1, 15))
        self.check('user-city: abc', conf)
        self.check('user-city: 010,0571', conf)
        self.check("user-city: '010'", conf)
        self.check('user-city: "010"', conf)
        self.check('user-city:\n'
                   '  - 010', conf, problem=(2, 8))
        self.check('user-city: [010]', conf, problem=(1, 16))
        self.check('user-city: {beijing: 010}', conf, problem=(1, 25))
        self.check('explicit-octal: 0o10', conf)
        self.check('not-number: 0abc', conf)
        self.check('zero: 0', conf)
        self.check('hex-value: 0x10', conf)
        self.check('number-values:\n'
                   '  - 0.10\n'
                   '  - .01\n'
                   '  - 0e3\n', conf)

    def test_explicit_octal_values(self):
        conf = ('octal-values:\n'
                '  forbid-implicit-octal: false\n'
                '  forbid-explicit-octal: true\n'
                'new-line-at-end-of-file: disable\n'
                'document-start: disable\n')
        self.check('user-city: 0o10', conf, problem=(1, 16))
        self.check('user-city: abc', conf)
        self.check('user-city: 0o10,0571', conf)
        self.check("user-city: '0o10'", conf)
        self.check('user-city:\n'
                   '  - 0o10', conf, problem=(2, 9))
        self.check('user-city: [0o10]', conf, problem=(1, 17))
        self.check('user-city: {beijing: 0o10}', conf, problem=(1, 26))
        self.check('implicit-octal: 010', conf)
        self.check('not-number: 0oabc', conf)
        self.check('zero: 0', conf)
        self.check('hex-value: 0x10', conf)
        self.check('number-values:\n'
                   '  - 0.10\n'
                   '  - .01\n'
                   '  - 0e3\n', conf)
        self.check('user-city: "010"', conf)
