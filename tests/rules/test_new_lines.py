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


class NewLinesTestCase(RuleTestCase):
    rule_id = 'new-lines'

    def test_disabled(self):
        conf = ('new-line-at-end-of-file: disable\n'
                'new-lines: disable\n')
        self.check('', conf)
        self.check('\n', conf)
        self.check('\r', conf)
        self.check('\r\n', conf)
        self.check('---\ntext\n', conf)
        self.check('---\r\ntext\r\n', conf)

    def test_unix_type(self):
        conf = ('new-line-at-end-of-file: disable\n'
                'new-lines: {type: unix}\n')
        self.check('', conf)
        self.check('\r', conf)
        self.check('\n', conf)
        self.check('\r\n', conf, problem=(1, 1))
        self.check('---\ntext\n', conf)
        self.check('---\r\ntext\r\n', conf, problem=(1, 4))

    def test_dos_type(self):
        conf = ('new-line-at-end-of-file: disable\n'
                'new-lines: {type: dos}\n')
        self.check('', conf)
        self.check('\r', conf)
        self.check('\n', conf, problem=(1, 1))
        self.check('\r\n', conf)
        self.check('---\ntext\n', conf, problem=(1, 4))
        self.check('---\r\ntext\r\n', conf)
