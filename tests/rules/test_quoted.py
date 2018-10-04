# -*- coding: utf-8 -*-
# Copyright (C) 2018 ClearScore
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


class QuotedTestCase(RuleTestCase):
    rule_id = 'quoted'

    def test_disabled(self):
        conf = 'quoted: disable'
        self.check('---\n'
                   'foo: bar\n', conf)
        self.check('---\n'
                   'bar: 123\n', conf)

    def test_quote_type_any(self):
        conf = 'quoted: {quote-type: any}\n'
        self.check('---\n'
                   'string1: "foo"\n'
                   'number1: 123\n'
                   'string2: foo\n'
                   'string3: \'yes\'\n',
                   conf, problem1=(3, 10), problem2=(4, 10))

    def test_quote_type_single(self):
        conf = 'quoted: {quote-type: single}\n'
        self.check('---\n'
                   'string1: \'foo\'\n'
                   'number1: 123\n'
                   'string2: foo\n'
                   'string3: "yes"\n',
                   conf, problem1=(3, 10), problem2=(4, 10), problem3=(5, 10))

    def test_quote_type_double(self):
        conf = 'quoted: {quote-type: double}\n'
        self.check('---\n'
                   'string1: "foo"\n'
                   'number1: 123\n'
                   'string2: foo\n'
                   'string3: \'yes\'\n',
                   conf, problem1=(3, 10), problem2=(4, 10), problem3=(5, 10))
