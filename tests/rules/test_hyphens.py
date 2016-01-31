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


class HyphenTestCase(RuleTestCase):
    rule_id = 'hyphens'

    def test_disabled(self):
        conf = 'hyphens: disable'
        self.check('---\n'
                   '- elem1\n'
                   '- elem2\n', conf)
        self.check('---\n'
                   '- elem1\n'
                   '-  elem2\n', conf)
        self.check('---\n'
                   '-  elem1\n'
                   '-  elem2\n', conf)
        self.check('---\n'
                   '-  elem1\n'
                   '- elem2\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  - elem1\n'
                   '  -  elem2\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  -  elem1\n'
                   '  -  elem2\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  subobject:\n'
                   '    - elem1\n'
                   '    -  elem2\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  subobject:\n'
                   '    -  elem1\n'
                   '    -  elem2\n', conf)

    def test_enabled(self):
        conf = 'hyphens: {max-spaces-after: 1}'
        self.check('---\n'
                   '- elem1\n'
                   '- elem2\n', conf)
        self.check('---\n'
                   '- elem1\n'
                   '-  elem2\n', conf, problem=(3, 3))
        self.check('---\n'
                   '-  elem1\n'
                   '-  elem2\n', conf, problem1=(2, 3), problem2=(3, 3))
        self.check('---\n'
                   '-  elem1\n'
                   '- elem2\n', conf, problem=(2, 3))
        self.check('---\n'
                   'object:\n'
                   '  - elem1\n'
                   '  -  elem2\n', conf, problem=(4, 5))
        self.check('---\n'
                   'object:\n'
                   '  -  elem1\n'
                   '  -  elem2\n', conf, problem1=(3, 5), problem2=(4, 5))
        self.check('---\n'
                   'object:\n'
                   '  subobject:\n'
                   '    - elem1\n'
                   '    -  elem2\n', conf, problem=(5, 7))
        self.check('---\n'
                   'object:\n'
                   '  subobject:\n'
                   '    -  elem1\n'
                   '    -  elem2\n', conf, problem1=(4, 7), problem2=(5, 7))

    def test_max_3(self):
        conf = 'hyphens: {max-spaces-after: 3}'
        self.check('---\n'
                   '-   elem1\n'
                   '-   elem2\n', conf)
        self.check('---\n'
                   '-    elem1\n'
                   '-   elem2\n', conf, problem=(2, 5))
        self.check('---\n'
                   'a:\n'
                   '  b:\n'
                   '    -   elem1\n'
                   '    -   elem2\n', conf)
        self.check('---\n'
                   'a:\n'
                   '  b:\n'
                   '    -    elem1\n'
                   '    -    elem2\n', conf, problem1=(4, 9), problem2=(5, 9))
