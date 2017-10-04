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


class DocumentStartTestCase(RuleTestCase):
    rule_id = 'document-start'

    def test_disabled(self):
        conf = 'document-start: disable'
        self.check('', conf)
        self.check('key: val\n', conf)
        self.check('---\n'
                   'key: val\n', conf)

    def test_required(self):
        conf = ('document-start: {present: true}\n'
                'empty-lines: disable\n')
        self.check('', conf)
        self.check('\n', conf)
        self.check('key: val\n', conf, problem=(1, 1))
        self.check('\n'
                   '\n'
                   'key: val\n', conf, problem=(3, 1))
        self.check('---\n'
                   'key: val\n', conf)
        self.check('\n'
                   '\n'
                   '---\n'
                   'key: val\n', conf)

    def test_forbidden(self):
        conf = ('document-start: {present: false}\n'
                'empty-lines: disable\n')
        self.check('', conf)
        self.check('key: val\n', conf)
        self.check('\n'
                   '\n'
                   'key: val\n', conf)
        self.check('---\n'
                   'key: val\n', conf, problem=(1, 1))
        self.check('\n'
                   '\n'
                   '---\n'
                   'key: val\n', conf, problem=(3, 1))
        self.check('first: document\n'
                   '---\n'
                   'key: val\n', conf, problem=(2, 1))

    def test_multiple_documents(self):
        conf = 'document-start: {present: true}'
        self.check('---\n'
                   'first: document\n'
                   '...\n'
                   '---\n'
                   'second: document\n'
                   '...\n'
                   '---\n'
                   'third: document\n', conf)
        self.check('---\n'
                   'first: document\n'
                   '---\n'
                   'second: document\n'
                   '---\n'
                   'third: document\n', conf)
        self.check('---\n'
                   'first: document\n'
                   '...\n'
                   'second: document\n'
                   '---\n'
                   'third: document\n', conf, problem=(4, 1, 'syntax'))

    def test_directives(self):
        conf = 'document-start: {present: true}'
        self.check('%YAML 1.2\n'
                   '---\n'
                   'doc: ument\n'
                   '...\n', conf)
        self.check('%YAML 1.2\n'
                   '%TAG ! tag:clarkevans.com,2002:\n'
                   '---\n'
                   'doc: ument\n'
                   '...\n', conf)
        self.check('---\n'
                   'doc: 1\n'
                   '...\n'
                   '%YAML 1.2\n'
                   '---\n'
                   'doc: 2\n'
                   '...\n', conf)
