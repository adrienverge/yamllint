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

import yaml

from tests.rules.common import RuleTestCase
from yamllint.rules.inline_comments import (Comment,
                                            get_comments_until_next_token)


class CommentsTestCase(RuleTestCase):
    rule_id = 'comments'

    def check_comments(self, buffer, *expected):
        yaml_loader = yaml.BaseLoader(buffer)

        comments = []

        next = yaml_loader.peek_token()
        while next is not None:
            curr = yaml_loader.get_token()
            next = yaml_loader.peek_token()
            for comment in get_comments_until_next_token(curr, next):
                comments.append(comment)

        self.assertEqual(comments, list(expected))

    def test_get_comments_until_next_token(self):
        self.check_comments('# comment\n',
                            Comment(1, 1, '# comment', 0))
        self.check_comments('---\n'
                            '# comment\n'
                            '...\n',
                            Comment(2, 1, '# comment', 0))
        self.check_comments('---\n'
                            '# no newline char',
                            Comment(2, 1, '# no newline char', 0))
        self.check_comments('\n'
                            '   # indented comment\n',
                            Comment(2, 4, '# indented comment', 0))
        self.check_comments('\n'
                            '# trailing spaces    \n',
                            Comment(2, 1, '# trailing spaces    ', 0))
        self.check_comments('# comment one\n'
                            '\n'
                            'key: val  # key=val\n'
                            '\n'
                            '# this is\n'
                            '# a block     \n'
                            '# comment\n'
                            '\n'
                            'other:\n'
                            '  - foo  # equals\n'
                            '         # bar\n',
                            Comment(1, 1, '# comment one', 0),
                            Comment(3, 11, '# key=val', 0),
                            Comment(5, 1, '# this is', 0),
                            Comment(6, 1, '# a block     ', 0),
                            Comment(7, 1, '# comment', 0),
                            Comment(10, 10, '# equals', 0),
                            Comment(11, 10, '# bar', 0))

    def test_disabled(self):
        conf = 'comments: disable'
        self.check('---\n'
                   '#comment\n'
                   '\n'
                   'test: #    description\n'
                   '  - foo  # bar\n'
                   '  - hello #world\n'
                   '\n'
                   '# comment 2\n'
                   '#comment 3\n'
                   '  #comment 3 bis\n'
                   '  #  comment 3 ter\n'
                   '\n'
                   'string: "Une longue phrase." # this is French\n', conf)

    def test_starting_space(self):
        conf = ('comments:\n'
                '  require-starting-space: yes\n'
                '  min-spaces-from-content: -1\n')
        self.check('---\n'
                   '# comment\n'
                   '\n'
                   'test:  #     description\n'
                   '  - foo  #   bar\n'
                   '  - hello  # world\n'
                   '\n'
                   '# comment 2\n'
                   '# comment 3\n'
                   '  #  comment 3 bis\n'
                   '  #  comment 3 ter\n', conf)
        self.check('---\n'
                   '#comment\n'
                   '\n'
                   'test:  #    description\n'
                   '  - foo  #  bar\n'
                   '  - hello  #world\n'
                   '\n'
                   '# comment 2\n'
                   '#comment 3\n'
                   '  #comment 3 bis\n'
                   '  #  comment 3 ter\n', conf,
                   problem1=(2, 2), problem2=(6, 13),
                   problem4=(9, 2), problem5=(10, 4))

    def test_spaces_from_content(self):
        conf = ('comments:\n'
                '  require-starting-space: no\n'
                '  min-spaces-from-content: 2\n')
        self.check('---\n'
                   '# comment\n'
                   '\n'
                   'test:  #    description\n'
                   '  - foo  #  bar\n'
                   '  - hello  #world\n'
                   '\n'
                   'string: "Une longue phrase."  # this is French\n', conf)
        self.check('---\n'
                   '# comment\n'
                   '\n'
                   'test: #    description\n'
                   '  - foo  # bar\n'
                   '  - hello #world\n'
                   '\n'
                   'string: "Une longue phrase." # this is French\n', conf,
                   problem1=(4, 7), problem2=(6, 11), problem3=(8, 30))

    def test_both(self):
        conf = ('comments:\n'
                '  require-starting-space: yes\n'
                '  min-spaces-from-content: 2\n')
        self.check('---\n'
                   '#comment\n'
                   '\n'
                   'test: #    description\n'
                   '  - foo  # bar\n'
                   '  - hello #world\n'
                   '\n'
                   '# comment 2\n'
                   '#comment 3\n'
                   '  #comment 3 bis\n'
                   '  #  comment 3 ter\n'
                   '\n'
                   'string: "Une longue phrase." # this is French\n', conf,
                   problem1=(2, 2),
                   problem2=(4, 7),
                   problem3=(6, 11), problem4=(6, 12),
                   problem5=(9, 2),
                   problem6=(10, 4),
                   problem7=(13, 30))
