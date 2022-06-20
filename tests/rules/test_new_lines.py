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

from unittest import mock

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

    def test_unix_type_required_st_sp(self):
        # If we find a CRLF when looking for Unix newlines, yamllint
        # should always raise, regardless of logic with
        # require-starting-space.
        conf = ('new-line-at-end-of-file: disable\n'
                'new-lines: {type: unix}\n'
                'comments:\n'
                '  require-starting-space: true\n')
        self.check('---\r\n#\r\n', conf, problem=(1, 4))

    def test_dos_type(self):
        conf = ('new-line-at-end-of-file: disable\n'
                'new-lines: {type: dos}\n')
        self.check('', conf)
        self.check('\r', conf)
        self.check('\n', conf, problem=(1, 1))
        self.check('\r\n', conf)
        self.check('---\ntext\n', conf, problem=(1, 4))
        self.check('---\r\ntext\r\n', conf)

    def test_platform_type(self):
        conf = ('new-line-at-end-of-file: disable\n'
                'new-lines: {type: platform}\n')

        self.check('', conf)

        # mock the Linux new-line-character
        with mock.patch('yamllint.rules.new_lines.linesep', '\n'):
            self.check('\n', conf)
            self.check('\r\n', conf, problem=(1, 1))
            self.check('---\ntext\n', conf)
            self.check('---\r\ntext\r\n', conf, problem=(1, 4))
            self.check('---\r\ntext\n', conf, problem=(1, 4))
            # FIXME: the following tests currently don't work
            # because only the first line is checked for line-endings
            # see: issue #475
            # ---
            # self.check('---\ntext\r\nfoo\n', conf, problem=(2, 4))
            # self.check('---\ntext\r\n', conf, problem=(2, 4))

        # mock the Windows new-line-character
        with mock.patch('yamllint.rules.new_lines.linesep', '\r\n'):
            self.check('\r\n', conf)
            self.check('\n', conf, problem=(1, 1))
            self.check('---\r\ntext\r\n', conf)
            self.check('---\ntext\n', conf, problem=(1, 4))
            self.check('---\ntext\r\n', conf, problem=(1, 4))
            # FIXME: the following tests currently don't work
            # because only the first line is checked for line-endings
            # see: issue #475
            # ---
            # self.check('---\r\ntext\nfoo\r\n', conf, problem=(2, 4))
            # self.check('---\r\ntext\n', conf, problem=(2, 4))
