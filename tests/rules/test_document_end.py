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


class DocumentEndTestCase(RuleTestCase):
    rule_id = 'document-end'

    def test_disabled(self):
        conf = 'document-end: disable'
        self.check('---\n'
                   'with:\n'
                   '  document: end\n'
                   '...\n', conf)
        self.check('---\n'
                   'without:\n'
                   '  document: end\n', conf)

    def test_required(self):
        conf = 'document-end: {present: true}'
        self.check('', conf)
        self.check('\n', conf)
        self.check('---\n'
                   'with:\n'
                   '  document: end\n'
                   '...\n', conf)
        self.check('---\n'
                   'without:\n'
                   '  document: end\n', conf, problem=(3, 1))

    def test_forbidden(self):
        conf = 'document-end: {present: false}'
        self.check('---\n'
                   'with:\n'
                   '  document: end\n'
                   '...\n', conf, problem=(4, 1))
        self.check('---\n'
                   'without:\n'
                   '  document: end\n', conf)

    def test_multiple_documents(self):
        conf = ('document-end: {present: true}\n'
                'document-start: disable\n')
        self.check('---\n'
                   'first: document\n'
                   '...\n'
                   '---\n'
                   'second: document\n'
                   '...\n'
                   '---\n'
                   'third: document\n'
                   '...\n', conf)
        self.check('---\n'
                   'first: document\n'
                   '...\n'
                   '---\n'
                   'second: document\n'
                   '---\n'
                   'third: document\n'
                   '...\n', conf, problem=(6, 1))
