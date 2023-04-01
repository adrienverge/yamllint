# Copyright (C) 2023 Adrien Vergé
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


class AnchorsTestCase(RuleTestCase):
    rule_id = 'anchors'

    def test_disabled(self):
        conf = 'anchors: disable'
        self.check('---\n'
                   '- &b true\n'
                   '- &i 42\n'
                   '- &s hello\n'
                   '- &f_m {k: v}\n'
                   '- &f_s [1, 2]\n'
                   '- *b\n'
                   '- *i\n'
                   '- *s\n'
                   '- *f_m\n'
                   '- *f_s\n'
                   '---\n'  # redeclare anchors in a new document
                   '- &b true\n'
                   '- &i 42\n'
                   '- &s hello\n'
                   '- *b\n'
                   '- *i\n'
                   '- *s\n'
                   '---\n'
                   'block mapping: &b_m\n'
                   '  key: value\n'
                   'extended:\n'
                   '  <<: *b_m\n'
                   '  foo: bar\n'
                   '---\n'
                   '{a: 1, &x b: 2, c: &y 3, *x : 4, e: *y}\n'
                   '...\n', conf)
        self.check('---\n'
                   '- &i 42\n'
                   '---\n'
                   '- &b true\n'
                   '- &b true\n'
                   '- &b true\n'
                   '- &s hello\n'
                   '- *b\n'
                   '- *i\n'    # declared in a previous document
                   '- *f_m\n'  # never declared
                   '- *f_m\n'
                   '- *f_m\n'
                   '- *f_s\n'  # declared after
                   '- &f_s [1, 2]\n'
                   '---\n'
                   'block mapping: &b_m\n'
                   '  key: value\n'
                   '---\n'
                   'block mapping 1: &b_m_bis\n'
                   '  key: value\n'
                   'block mapping 2: &b_m_bis\n'
                   '  key: value\n'
                   'extended:\n'
                   '  <<: *b_m\n'
                   '  foo: bar\n'
                   '---\n'
                   '{a: 1, &x b: 2, c: &x 3, *x : 4, e: *y}\n'
                   '...\n', conf)

    def test_forbid_undeclared_aliases(self):
        conf = ('anchors:\n'
                '  forbid-undeclared-aliases: true\n'
                '  forbid-duplicated-anchors: false\n'
                '  forbid-unused-anchors: false\n')
        self.check('---\n'
                   '- &b true\n'
                   '- &i 42\n'
                   '- &s hello\n'
                   '- &f_m {k: v}\n'
                   '- &f_s [1, 2]\n'
                   '- *b\n'
                   '- *i\n'
                   '- *s\n'
                   '- *f_m\n'
                   '- *f_s\n'
                   '---\n'  # redeclare anchors in a new document
                   '- &b true\n'
                   '- &i 42\n'
                   '- &s hello\n'
                   '- *b\n'
                   '- *i\n'
                   '- *s\n'
                   '---\n'
                   'block mapping: &b_m\n'
                   '  key: value\n'
                   'extended:\n'
                   '  <<: *b_m\n'
                   '  foo: bar\n'
                   '---\n'
                   '{a: 1, &x b: 2, c: &y 3, *x : 4, e: *y}\n'
                   '...\n', conf)
        self.check('---\n'
                   '- &i 42\n'
                   '---\n'
                   '- &b true\n'
                   '- &b true\n'
                   '- &b true\n'
                   '- &s hello\n'
                   '- *b\n'
                   '- *i\n'    # declared in a previous document
                   '- *f_m\n'  # never declared
                   '- *f_m\n'
                   '- *f_m\n'
                   '- *f_s\n'  # declared after
                   '- &f_s [1, 2]\n'
                   '...\n'
                   '---\n'
                   'block mapping: &b_m\n'
                   '  key: value\n'
                   '---\n'
                   'block mapping 1: &b_m_bis\n'
                   '  key: value\n'
                   'block mapping 2: &b_m_bis\n'
                   '  key: value\n'
                   'extended:\n'
                   '  <<: *b_m\n'
                   '  foo: bar\n'
                   '---\n'
                   '{a: 1, &x b: 2, c: &x 3, *x : 4, e: *y}\n'
                   '...\n', conf,
                   problem1=(9, 3),
                   problem2=(10, 3),
                   problem3=(11, 3),
                   problem4=(12, 3),
                   problem5=(13, 3),
                   problem6=(25, 7),
                   problem7=(28, 37))

    def test_forbid_duplicated_anchors(self):
        conf = ('anchors:\n'
                '  forbid-undeclared-aliases: false\n'
                '  forbid-duplicated-anchors: true\n'
                '  forbid-unused-anchors: false\n')
        self.check('---\n'
                   '- &b true\n'
                   '- &i 42\n'
                   '- &s hello\n'
                   '- &f_m {k: v}\n'
                   '- &f_s [1, 2]\n'
                   '- *b\n'
                   '- *i\n'
                   '- *s\n'
                   '- *f_m\n'
                   '- *f_s\n'
                   '---\n'  # redeclare anchors in a new document
                   '- &b true\n'
                   '- &i 42\n'
                   '- &s hello\n'
                   '- *b\n'
                   '- *i\n'
                   '- *s\n'
                   '---\n'
                   'block mapping: &b_m\n'
                   '  key: value\n'
                   'extended:\n'
                   '  <<: *b_m\n'
                   '  foo: bar\n'
                   '---\n'
                   '{a: 1, &x b: 2, c: &y 3, *x : 4, e: *y}\n'
                   '...\n', conf)
        self.check('---\n'
                   '- &i 42\n'
                   '---\n'
                   '- &b true\n'
                   '- &b true\n'
                   '- &b true\n'
                   '- &s hello\n'
                   '- *b\n'
                   '- *i\n'    # declared in a previous document
                   '- *f_m\n'  # never declared
                   '- *f_m\n'
                   '- *f_m\n'
                   '- *f_s\n'  # declared after
                   '- &f_s [1, 2]\n'
                   '...\n'
                   '---\n'
                   'block mapping: &b_m\n'
                   '  key: value\n'
                   '---\n'
                   'block mapping 1: &b_m_bis\n'
                   '  key: value\n'
                   'block mapping 2: &b_m_bis\n'
                   '  key: value\n'
                   'extended:\n'
                   '  <<: *b_m\n'
                   '  foo: bar\n'
                   '---\n'
                   '{a: 1, &x b: 2, c: &x 3, *x : 4, e: *y}\n'
                   '...\n', conf,
                   problem1=(5, 3),
                   problem2=(6, 3),
                   problem3=(22, 18),
                   problem4=(28, 20))

    def test_forbid_unused_anchors(self):
        conf = ('anchors:\n'
                '  forbid-undeclared-aliases: false\n'
                '  forbid-duplicated-anchors: false\n'
                '  forbid-unused-anchors: true\n')

        self.check('---\n'
                   '- &b true\n'
                   '- &i 42\n'
                   '- &s hello\n'
                   '- &f_m {k: v}\n'
                   '- &f_s [1, 2]\n'
                   '- *b\n'
                   '- *i\n'
                   '- *s\n'
                   '- *f_m\n'
                   '- *f_s\n'
                   '---\n'  # redeclare anchors in a new document
                   '- &b true\n'
                   '- &i 42\n'
                   '- &s hello\n'
                   '- *b\n'
                   '- *i\n'
                   '- *s\n'
                   '---\n'
                   'block mapping: &b_m\n'
                   '  key: value\n'
                   'extended:\n'
                   '  <<: *b_m\n'
                   '  foo: bar\n'
                   '---\n'
                   '{a: 1, &x b: 2, c: &y 3, *x : 4, e: *y}\n'
                   '...\n', conf)
        self.check('---\n'
                   '- &i 42\n'
                   '---\n'
                   '- &b true\n'
                   '- &b true\n'
                   '- &b true\n'
                   '- &s hello\n'
                   '- *b\n'
                   '- *i\n'    # declared in a previous document
                   '- *f_m\n'  # never declared
                   '- *f_m\n'
                   '- *f_m\n'
                   '- *f_s\n'  # declared after
                   '- &f_s [1, 2]\n'
                   '...\n'
                   '---\n'
                   'block mapping: &b_m\n'
                   '  key: value\n'
                   '---\n'
                   'block mapping 1: &b_m_bis\n'
                   '  key: value\n'
                   'block mapping 2: &b_m_bis\n'
                   '  key: value\n'
                   'extended:\n'
                   '  <<: *b_m\n'
                   '  foo: bar\n'
                   '---\n'
                   '{a: 1, &x b: 2, c: &x 3, *x : 4, e: *y}\n'
                   '...\n', conf,
                   problem1=(2, 3),
                   problem2=(7, 3),
                   problem3=(14, 3),
                   problem4=(17, 16),
                   problem5=(22, 18))
