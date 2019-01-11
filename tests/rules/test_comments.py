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


class CommentsTestCase(RuleTestCase):
    rule_id = 'comments'

    def test_disabled(self):
        conf = ('comments: disable\n'
                'comments-indentation: disable\n')
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
                   '################################\n'
                   '## comment 4\n'
                   '##comment 5\n'
                   '\n'
                   'string: "Une longue phrase." # this is French\n', conf)

    def test_starting_space(self):
        conf = ('comments:\n'
                '  require-starting-space: true\n'
                '  min-spaces-from-content: -1\n'
                'comments-indentation: disable\n')
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
                   '  #  comment 3 ter\n'
                   '\n'
                   '################################\n'
                   '## comment 4\n'
                   '##  comment 5\n', conf)
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
                   '  #  comment 3 ter\n'
                   '\n'
                   '################################\n'
                   '## comment 4\n'
                   '##comment 5\n', conf,
                   problem1=(2, 2), problem2=(6, 13),
                   problem3=(9, 2), problem4=(10, 4),
                   problem5=(15, 3))

    def test_shebang(self):
        conf = ('comments:\n'
                '  require-starting-space: true\n'
                '  ignore-shebangs: false\n'
                'comments-indentation: disable\n'
                'document-start: disable\n')
        self.check('#!/bin/env my-interpreter\n',
                   conf, problem1=(1, 2))
        self.check('# comment\n'
                   '#!/bin/env my-interpreter\n', conf,
                   problem1=(2, 2))
        self.check('#!/bin/env my-interpreter\n'
                   '---\n'
                   '#comment\n'
                   '#!/bin/env my-interpreter\n'
                   '', conf,
                   problem1=(1, 2), problem2=(3, 2), problem3=(4, 2))
        self.check('#! not a shebang\n',
                   conf, problem1=(1, 2))
        self.check('key:  #!/not/a/shebang\n',
                   conf, problem1=(1, 8))

    def test_ignore_shebang(self):
        conf = ('comments:\n'
                '  require-starting-space: true\n'
                '  ignore-shebangs: true\n'
                'comments-indentation: disable\n'
                'document-start: disable\n')
        self.check('#!/bin/env my-interpreter\n', conf)
        self.check('# comment\n'
                   '#!/bin/env my-interpreter\n', conf,
                   problem1=(2, 2))
        self.check('#!/bin/env my-interpreter\n'
                   '---\n'
                   '#comment\n'
                   '#!/bin/env my-interpreter\n', conf,
                   problem2=(3, 2), problem3=(4, 2))
        self.check('#! not a shebang\n',
                   conf, problem1=(1, 2))
        self.check('key:  #!/not/a/shebang\n',
                   conf, problem1=(1, 8))

    def test_spaces_from_content(self):
        conf = ('comments:\n'
                '  require-starting-space: false\n'
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
                '  require-starting-space: true\n'
                '  min-spaces-from-content: 2\n'
                'comments-indentation: disable\n')
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
                   '################################\n'
                   '## comment 4\n'
                   '##comment 5\n'
                   '\n'
                   'string: "Une longue phrase." # this is French\n', conf,
                   problem1=(2, 2),
                   problem2=(4, 7),
                   problem3=(6, 11), problem4=(6, 12),
                   problem5=(9, 2),
                   problem6=(10, 4),
                   problem7=(15, 3),
                   problem8=(17, 30))

    def test_empty_comment(self):
        conf = ('comments:\n'
                '  require-starting-space: true\n'
                '  min-spaces-from-content: 2\n')
        self.check('---\n'
                   '# This is paragraph 1.\n'
                   '#\n'
                   '# This is paragraph 2.\n', conf)
        self.check('---\n'
                   'inline: comment  #\n'
                   'foo: bar\n', conf)

    def test_first_line(self):
        conf = ('comments:\n'
                '  require-starting-space: true\n'
                '  min-spaces-from-content: 2\n')
        self.check('# comment\n', conf)

    def test_last_line(self):
        conf = ('comments:\n'
                '  require-starting-space: true\n'
                '  min-spaces-from-content: 2\n'
                'new-line-at-end-of-file: disable\n')
        self.check('# comment with no newline char:\n'
                   '#', conf)

    def test_multi_line_scalar(self):
        conf = ('comments:\n'
                '  require-starting-space: true\n'
                '  min-spaces-from-content: 2\n'
                'trailing-spaces: disable\n')
        self.check('---\n'
                   'string: >\n'
                   '  this is plain text\n'
                   '\n'
                   '# comment\n', conf)
        self.check('---\n'
                   '- string: >\n'
                   '    this is plain text\n'
                   '  \n'
                   '  # comment\n', conf)
