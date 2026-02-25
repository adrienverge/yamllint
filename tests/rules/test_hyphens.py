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

from yamllint import config


class HyphenTestCase(RuleTestCase):
    rule_id = 'hyphens'

    def test_disabled(self):
        self.run_disabled_test('hyphens: disable')
        self.run_disabled_test('hyphens:\n'
                               '  max-spaces-after: 5\n'
                               '  min-spaces-after: -1\n')
        self.run_disabled_test('hyphens:\n'
                               '  max-spaces-after: -1\n'
                               '  min-spaces-after: -1\n')
        self.run_disabled_test('hyphens:\n'
                               '  max-spaces-after: -1\n'
                               '  min-spaces-after: 0\n')

    def run_disabled_test(self, conf):
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
        self.check('---\n'
                   'object:\n'
                   '  -elem2\n', conf)

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

    def test_invalid_spaces(self):
        conf = 'hyphens: {max-spaces-after: 0}'
        self.assertRaises(config.YamlLintConfigError, self.check, '', conf)

        conf = 'hyphens: {min-spaces-after: 3}'
        self.assertRaises(config.YamlLintConfigError, self.check, '', conf)

    def test_min_space(self):
        conf = 'hyphens: {max-spaces-after: 4, min-spaces-after: 3}'
        self.check('---\n'
                   'object:\n'
                   '  -   elem1\n'
                   '  -   elem2\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  -    elem1\n'
                   '  -    elem2: -foo\n'
                   '-bar:\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  -  elem1\n'
                   '  -  elem2\n', conf, problem1=(3, 6), problem2=(4, 6))

        conf = ('hyphens:\n'
                '  max-spaces-after: 4\n'
                '  min-spaces-after: 3\n'
                '  check-scalars: true\n')
        self.check('---\n'
                   'foo\n'
                   '-bar\n', conf)
        self.check('---\n'
                   'object:\n'
                   '  -    elem1\n'
                   '  -    elem2\n'
                   'key: -value\n', conf, problem=(5, 6))
        self.check('---\n'
                   'list:\n'
                   '  -value\n', conf, problem=(3, 3))
