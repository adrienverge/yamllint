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


class NewLineAtEndOfFileTestCase(RuleTestCase):
    rule_id = 'new-line-at-end-of-file'

    def test_disabled(self):
        conf = ('new-line-at-end-of-file: disable\n'
                'empty-lines: disable\n'
                'document-start: disable\n')
        self.check('', conf)
        self.check('\n', conf)
        self.check('word', conf)
        self.check('Sentence.\n', conf)

    def test_enabled(self):
        conf = ('new-line-at-end-of-file: enable\n'
                'empty-lines: disable\n'
                'document-start: disable\n')
        self.check('', conf)
        self.check('\n', conf)
        self.check('word', conf, problem=(1, 5))
        self.check('Sentence.\n', conf)
        self.check('---\n'
                   'yaml: document\n'
                   '...', conf, problem=(3, 4))
