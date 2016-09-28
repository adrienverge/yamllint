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


class CommentsIndentationTestCase(RuleTestCase):
    rule_id = 'comments-indentation'

    def test_disable(self):
        conf = 'comments-indentation: disable'
        self.check('---\n'
                   ' # line 1\n'
                   '# line 2\n'
                   '  # line 3\n'
                   '  # line 4\n'
                   '\n'
                   'obj:\n'
                   ' # these\n'
                   '   # are\n'
                   '  # [good]\n'
                   '# bad\n'
                   '      # comments\n'
                   '  a: b\n'
                   '\n'
                   'obj1:\n'
                   '  a: 1\n'
                   '  # comments\n'
                   '\n'
                   'obj2:\n'
                   '  b: 2\n'
                   '\n'
                   '# empty\n'
                   '#\n'
                   '# comment\n'
                   '...\n', conf)

    def test_enabled(self):
        conf = 'comments-indentation: enable'
        self.check('---\n'
                   '# line 1\n'
                   '# line 2\n', conf)
        self.check('---\n'
                   ' # line 1\n'
                   '# line 2\n', conf, problem=(2, 2))
        self.check('---\n'
                   '  # line 1\n'
                   '  # line 2\n', conf, problem1=(2, 3))
        self.check('---\n'
                   'obj:\n'
                   '  # normal\n'
                   '  a: b\n', conf)
        self.check('---\n'
                   'obj:\n'
                   ' # bad\n'
                   '  a: b\n', conf, problem=(3, 2))
        self.check('---\n'
                   'obj:\n'
                   '# bad\n'
                   '  a: b\n', conf, problem=(3, 1))
        self.check('---\n'
                   'obj:\n'
                   '   # bad\n'
                   '  a: b\n', conf, problem=(3, 4))
        self.check('---\n'
                   'obj:\n'
                   ' # these\n'
                   '   # are\n'
                   '  # [good]\n'
                   '# bad\n'
                   '      # comments\n'
                   '  a: b\n', conf,
                   problem1=(3, 2), problem2=(4, 4),
                   problem3=(6, 1), problem4=(7, 7))
        self.check('---\n'
                   'obj1:\n'
                   '  a: 1\n'
                   '  # the following line is disabled\n'
                   '  # b: 2\n', conf)
        self.check('---\n'
                   'obj1:\n'
                   '  a: 1\n'
                   '  # b: 2\n'
                   '\n'
                   'obj2:\n'
                   '  b: 2\n', conf)
        self.check('---\n'
                   'obj1:\n'
                   '  a: 1\n'
                   '  # b: 2\n'
                   '# this object is useless\n'
                   'obj2: "no"\n', conf)
        self.check('---\n'
                   'obj1:\n'
                   '  a: 1\n'
                   '# this object is useless\n'
                   '  # b: 2\n'
                   'obj2: "no"\n', conf, problem=(5, 3))
        self.check('---\n'
                   'obj1:\n'
                   '  a: 1\n'
                   '  # comments\n'
                   '  b: 2\n', conf)
        self.check('---\n'
                   'my list for today:\n'
                   '  - todo 1\n'
                   '  - todo 2\n'
                   '  # commented for now\n'
                   '  # - todo 3\n'
                   '...\n', conf)

    def test_first_line(self):
        conf = 'comments-indentation: enable'
        self.check('# comment\n', conf)
        self.check('  # comment\n', conf, problem=(1, 3))

    def test_no_newline_at_end(self):
        conf = ('comments-indentation: enable\n'
                'new-line-at-end-of-file: disable\n')
        self.check('# comment', conf)
        self.check('  # comment', conf, problem=(1, 3))

    def test_empty_comment(self):
        conf = 'comments-indentation: enable'
        self.check('---\n'
                   '# hey\n'
                   '# normal\n'
                   '#\n', conf)
        self.check('---\n'
                   '# hey\n'
                   '# normal\n'
                   ' #\n', conf, problem=(4, 2))

    def test_inline_comment(self):
        conf = 'comments-indentation: enable'
        self.check('---\n'
                   '- a  # inline\n'
                   '# ok\n', conf)
        self.check('---\n'
                   '- a  # inline\n'
                   ' # not ok\n', conf, problem=(3, 2))
        self.check('---\n'
                   ' # not ok\n'
                   '- a  # inline\n', conf, problem=(2, 2))
