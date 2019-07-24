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

import sys
import unittest

from tests.common import RuleTestCase


class LineLengthTestCase(RuleTestCase):
    rule_id = 'line-length'

    def test_disabled(self):
        conf = ('line-length: disable\n'
                'empty-lines: disable\n'
                'new-line-at-end-of-file: disable\n'
                'document-start: disable\n')
        self.check('', conf)
        self.check('\n', conf)
        self.check('---\n', conf)
        self.check(81 * 'a', conf)
        self.check('---\n' + 81 * 'a' + '\n', conf)
        self.check(1000 * 'b', conf)
        self.check('---\n' + 1000 * 'b' + '\n', conf)
        self.check('content: |\n'
                   '  {% this line is' + 99 * ' really' + ' long %}\n',
                   conf)

    def test_default(self):
        conf = ('line-length: {max: 80}\n'
                'empty-lines: disable\n'
                'new-line-at-end-of-file: disable\n'
                'document-start: disable\n')
        self.check('', conf)
        self.check('\n', conf)
        self.check('---\n', conf)
        self.check(80 * 'a', conf)
        self.check('---\n' + 80 * 'a' + '\n', conf)
        self.check(16 * 'aaaa ' + 'z', conf, problem=(1, 81))
        self.check('---\n' + 16 * 'aaaa ' + 'z' + '\n', conf, problem=(2, 81))
        self.check(1000 * 'word ' + 'end', conf, problem=(1, 81))
        self.check('---\n' + 1000 * 'word ' + 'end\n', conf, problem=(2, 81))

    def test_max_length_10(self):
        conf = ('line-length: {max: 10}\n'
                'new-line-at-end-of-file: disable\n')
        self.check('---\nABCD EFGHI', conf)
        self.check('---\nABCD EFGHIJ', conf, problem=(2, 11))
        self.check('---\nABCD EFGHIJ\n', conf, problem=(2, 11))

    def test_spaces(self):
        conf = ('line-length: {max: 80}\n'
                'new-line-at-end-of-file: disable\n'
                'trailing-spaces: disable\n')
        self.check('---\n' + 81 * ' ', conf, problem=(2, 81))
        self.check('---\n' + 81 * ' ' + '\n', conf, problem=(2, 81))

    def test_non_breakable_word(self):
        conf = 'line-length: {max: 20, allow-non-breakable-words: true}'
        self.check('---\n' + 30 * 'A' + '\n', conf)
        self.check('---\n'
                   'this:\n'
                   '  is:\n'
                   '    - a:\n'
                   '        http://localhost/very/long/url\n'
                   '...\n', conf)
        self.check('---\n'
                   'this:\n'
                   '  is:\n'
                   '    - a:\n'
                   '        # http://localhost/very/long/url\n'
                   '        comment\n'
                   '...\n', conf)
        self.check('---\n'
                   'this:\n'
                   'is:\n'
                   'another:\n'
                   '  - https://localhost/very/very/long/url\n'
                   '...\n', conf)
        self.check('---\n'
                   'long_line: http://localhost/very/very/long/url\n', conf,
                   problem=(2, 21))

        conf = 'line-length: {max: 20, allow-non-breakable-words: false}'
        self.check('---\n' + 30 * 'A' + '\n', conf, problem=(2, 21))
        self.check('---\n'
                   'this:\n'
                   '  is:\n'
                   '    - a:\n'
                   '        http://localhost/very/long/url\n'
                   '...\n', conf, problem=(5, 21))
        self.check('---\n'
                   'this:\n'
                   '  is:\n'
                   '    - a:\n'
                   '        # http://localhost/very/long/url\n'
                   '        comment\n'
                   '...\n', conf, problem=(5, 21))
        self.check('---\n'
                   'this:\n'
                   'is:\n'
                   'another:\n'
                   '  - https://localhost/very/very/long/url\n'
                   '...\n', conf, problem=(5, 21))
        self.check('---\n'
                   'long_line: http://localhost/very/very/long/url\n'
                   '...\n', conf, problem=(2, 21))

        conf = ('line-length: {max: 20, allow-non-breakable-words: true}\n'
                'trailing-spaces: disable')
        self.check('---\n'
                   'loooooooooong+word+and+some+space+at+the+end       \n',
                   conf, problem=(2, 21))

    def test_non_breakable_inline_mappings(self):
        conf = 'line-length: {max: 20, ' \
               'allow-non-breakable-inline-mappings: true}'
        self.check('---\n'
                   'long_line: http://localhost/very/very/long/url\n'
                   'long line: http://localhost/very/very/long/url\n', conf)
        self.check('---\n'
                   '- long line: http://localhost/very/very/long/url\n', conf)

        self.check('---\n'
                   'long_line: http://localhost/short/url + word\n'
                   'long line: http://localhost/short/url + word\n',
                   conf, problem1=(2, 21), problem2=(3, 21))

        conf = ('line-length: {max: 20,'
                '              allow-non-breakable-inline-mappings: true}\n'
                'trailing-spaces: disable')
        self.check('---\n'
                   'long_line: and+some+space+at+the+end       \n',
                   conf, problem=(2, 21))
        self.check('---\n'
                   'long line: and+some+space+at+the+end       \n',
                   conf, problem=(2, 21))
        self.check('---\n'
                   '- long line: and+some+space+at+the+end       \n',
                   conf, problem=(2, 21))

        # See https://github.com/adrienverge/yamllint/issues/21
        conf = 'line-length: {allow-non-breakable-inline-mappings: true}'
        self.check('---\n'
                   'content: |\n'
                   '  {% this line is' + 99 * ' really' + ' long %}\n',
                   conf, problem=(3, 81))

    @unittest.skipIf(sys.version_info < (3, 0), 'Python 2 not supported')
    def test_unicode(self):
        conf = 'line-length: {max: 53}'
        self.check('---\n'
                   '# This is a test to check if “line-length” works nice\n'
                   'with: “unicode characters” that span accross bytes! ↺\n',
                   conf)
        conf = 'line-length: {max: 52}'
        self.check('---\n'
                   '# This is a test to check if “line-length” works nice\n'
                   'with: “unicode characters” that span accross bytes! ↺\n',
                   conf, problem1=(2, 53), problem2=(3, 53))

    def test_with_dos_newlines(self):
        conf = ('line-length: {max: 10}\n'
                'new-lines: {type: dos}\n'
                'new-line-at-end-of-file: disable\n')
        self.check('---\r\nABCD EFGHI', conf)
        self.check('---\r\nABCD EFGHI\r\n', conf)
        self.check('---\r\nABCD EFGHIJ', conf, problem=(2, 11))
        self.check('---\r\nABCD EFGHIJ\r\n', conf, problem=(2, 11))
