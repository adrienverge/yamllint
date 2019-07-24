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


class EmptyLinesTestCase(RuleTestCase):
    rule_id = 'empty-lines'

    def test_disabled(self):
        conf = ('empty-lines: disable\n'
                'new-line-at-end-of-file: disable\n'
                'document-start: disable\n')
        self.check('', conf)
        self.check('\n', conf)
        self.check('\n\n', conf)
        self.check('\n\n\n\n\n\n\n\n\n', conf)
        self.check('some text\n\n\n\n\n\n\n\n\n', conf)
        self.check('\n\n\n\n\n\n\n\n\nsome text', conf)
        self.check('\n\n\nsome text\n\n\n', conf)

    def test_empty_document(self):
        conf = ('empty-lines: {max: 0, max-start: 0, max-end: 0}\n'
                'new-line-at-end-of-file: disable\n'
                'document-start: disable\n')
        self.check('', conf)
        self.check('\n', conf)

    def test_0_empty_lines(self):
        conf = ('empty-lines: {max: 0, max-start: 0, max-end: 0}\n'
                'new-line-at-end-of-file: disable\n')
        self.check('---\n', conf)
        self.check('---\ntext\n\ntext', conf, problem=(3, 1))
        self.check('---\ntext\n\ntext\n', conf, problem=(3, 1))

    def test_10_empty_lines(self):
        conf = 'empty-lines: {max: 10, max-start: 0, max-end: 0}'
        self.check('---\nintro\n\n\n\n\n\n\n\n\n\n\nconclusion\n', conf)
        self.check('---\nintro\n\n\n\n\n\n\n\n\n\n\n\nconclusion\n', conf,
                   problem=(13, 1))

    def test_spaces(self):
        conf = ('empty-lines: {max: 1, max-start: 0, max-end: 0}\n'
                'trailing-spaces: disable\n')
        self.check('---\nintro\n\n \n\nconclusion\n', conf)
        self.check('---\nintro\n\n \n\n\nconclusion\n', conf, problem=(6, 1))

    def test_empty_lines_at_start(self):
        conf = ('empty-lines: {max: 2, max-start: 4, max-end: 0}\n'
                'document-start: disable\n')
        self.check('\n\n\n\nnon empty\n', conf)
        self.check('\n\n\n\n\nnon empty\n', conf, problem=(5, 1))

        conf = ('empty-lines: {max: 2, max-start: 0, max-end: 0}\n'
                'document-start: disable\n')
        self.check('non empty\n', conf)
        self.check('\nnon empty\n', conf, problem=(1, 1))

    def test_empty_lines_at_end(self):
        conf = ('empty-lines: {max: 2, max-start: 0, max-end: 4}\n'
                'document-start: disable\n')
        self.check('non empty\n\n\n\n\n', conf)
        self.check('non empty\n\n\n\n\n\n', conf, problem=(6, 1))
        conf = ('empty-lines: {max: 2, max-start: 0, max-end: 0}\n'
                'document-start: disable\n')
        self.check('non empty\n', conf)
        self.check('non empty\n\n', conf, problem=(2, 1))

    def test_with_dos_newlines(self):
        conf = ('empty-lines: {max: 2, max-start: 0, max-end: 0}\n'
                'new-lines: {type: dos}\n'
                'document-start: disable\n')
        self.check('---\r\n', conf)
        self.check('---\r\ntext\r\n\r\ntext\r\n', conf)
        self.check('\r\n---\r\ntext\r\n\r\ntext\r\n', conf,
                   problem=(1, 1))
        self.check('\r\n\r\n\r\n---\r\ntext\r\n\r\ntext\r\n', conf,
                   problem=(3, 1))
        self.check('---\r\ntext\r\n\r\n\r\n\r\ntext\r\n', conf,
                   problem=(5, 1))
        self.check('---\r\ntext\r\n\r\n\r\n\r\n\r\n\r\n\r\ntext\r\n', conf,
                   problem=(8, 1))
        self.check('---\r\ntext\r\n\r\ntext\r\n\r\n', conf,
                   problem=(5, 1))
        self.check('---\r\ntext\r\n\r\ntext\r\n\r\n\r\n\r\n', conf,
                   problem=(7, 1))
