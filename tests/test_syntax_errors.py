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


class YamlLintTestCase(RuleTestCase):
    rule_id = None  # syntax error

    def test_syntax_errors(self):
        self.check('---\n'
                   'this is not: valid: YAML\n', None, problem=(2, 19))
        self.check('---\n'
                   'this is: valid YAML\n'
                   '\n'
                   'this is an error: [\n'
                   '\n'
                   '...\n', None, problem=(6, 1))
        self.check('%YAML 1.2\n'
                   '%TAG ! tag:clarkevans.com,2002:\n'
                   'doc: ument\n'
                   '...\n', None, problem=(3, 1))

    def test_empty_flows(self):
        self.check('---\n'
                   '- []\n'
                   '- {}\n'
                   '- [\n'
                   ']\n'
                   '- {\n'
                   '}\n'
                   '...\n', None)

    def test_explicit_mapping(self):
        self.check('---\n'
                   '? key\n'
                   ': - value 1\n'
                   '  - value 2\n'
                   '...\n', None)
        self.check('---\n'
                   '?\n'
                   '  key\n'
                   ': {a: 1}\n'
                   '...\n', None)
        self.check('---\n'
                   '?\n'
                   '  key\n'
                   ':\n'
                   '  val\n'
                   '...\n', None)

    def test_mapping_between_sequences(self):
        # This is valid YAML. See http://www.yaml.org/spec/1.2/spec.html,
        # example 2.11
        self.check('---\n'
                   '? - Detroit Tigers\n'
                   '  - Chicago cubs\n'
                   ':\n'
                   '  - 2001-07-23\n'
                   '\n'
                   '? [New York Yankees,\n'
                   '   Atlanta Braves]\n'
                   ': [2001-07-02, 2001-08-12,\n'
                   '   2001-08-14]\n', None)

    def test_sets(self):
        self.check('---\n'
                   '? key one\n'
                   '? key two\n'
                   '? [non, scalar, key]\n'
                   '? key with value\n'
                   ': value\n'
                   '...\n', None)
        self.check('---\n'
                   '? - multi\n'
                   '  - line\n'
                   '  - keys\n'
                   '? in:\n'
                   '    a:\n'
                   '      set\n'
                   '...\n', None)
