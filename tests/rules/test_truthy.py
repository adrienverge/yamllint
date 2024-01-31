# Copyright (C) 2016 Peter Ericson
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


class TruthyTestCase(RuleTestCase):
    rule_id = 'truthy'

    def test_disabled(self):
        conf = 'truthy: disable'
        self.check('---\n'
                   '1: True\n', conf)
        self.check('---\n'
                   'True: 1\n', conf)

    def test_enabled(self):
        conf = ('truthy: enable\n'
                'document-start: disable\n')
        self.check('---\n'
                   '1: True\n'
                   'True: 1\n',
                   conf, problem1=(2, 4), problem2=(3, 1))
        self.check('---\n'
                   '1: "True"\n'
                   '"True": 1\n', conf)
        self.check('%YAML 1.1\n'
                   '---\n'
                   '[\n'
                   '  true, false,\n'
                   '  "false", "FALSE",\n'
                   '  "true", "True",\n'
                   '  True, FALSE,\n'
                   '  on, OFF,\n'
                   '  NO, Yes\n'
                   ']\n', conf,
                   problem1=(7, 3), problem2=(7, 9),
                   problem3=(8, 3), problem4=(8, 7),
                   problem5=(9, 3), problem6=(9, 7))
        self.check('y: 1\n'
                   'yes: 2\n'
                   'on: 3\n'
                   'true: 4\n'
                   'True: 5\n'
                   '...\n'
                   '%YAML 1.2\n'
                   '---\n'
                   'y: 1\n'
                   'yes: 2\n'
                   'on: 3\n'
                   'true: 4\n'
                   'True: 5\n'
                   '...\n'
                   '%YAML 1.1\n'
                   '---\n'
                   'y: 1\n'
                   'yes: 2\n'
                   'on: 3\n'
                   'true: 4\n'
                   'True: 5\n'
                   '---\n'
                   'y: 1\n'
                   'yes: 2\n'
                   'on: 3\n'
                   'true: 4\n'
                   'True: 5\n',
                   conf,
                   problem1=(2, 1),
                   problem2=(3, 1),
                   problem3=(5, 1),
                   problem4=(13, 1),
                   problem5=(18, 1),
                   problem6=(19, 1),
                   problem7=(21, 1),
                   problem8=(24, 1),
                   problem9=(25, 1),
                   problem10=(27, 1))

    def test_different_allowed_values(self):
        conf = ('truthy:\n'
                '  allowed-values: ["yes", "no"]\n')
        self.check('---\n'
                   'key1: foo\n'
                   'key2: yes\n'
                   'key3: bar\n'
                   'key4: no\n', conf)
        self.check('%YAML 1.1\n'
                   '---\n'
                   'key1: true\n'
                   'key2: Yes\n'
                   'key3: false\n'
                   'key4: no\n'
                   'key5: yes\n',
                   conf,
                   problem1=(3, 7), problem2=(4, 7),
                   problem3=(5, 7))

    def test_combined_allowed_values(self):
        conf = ('truthy:\n'
                '  allowed-values: ["yes", "no", "true", "false"]\n')
        self.check('---\n'
                   'key1: foo\n'
                   'key2: yes\n'
                   'key3: bar\n'
                   'key4: no\n', conf)
        self.check('---\n'
                   'key1: true\n'
                   'key2: Yes\n'
                   'key3: false\n'
                   'key4: no\n'
                   'key5: yes\n',
                   conf, problem1=(3, 7))
        self.check('%YAML 1.1\n'
                   '---\n'
                   'key1: true\n'
                   'key2: Yes\n'
                   'key3: false\n'
                   'key4: no\n'
                   'key5: yes\n',
                   conf, problem1=(4, 7))
        self.check('%YAML 1.2\n'
                   '---\n'
                   'key1: true\n'
                   'key2: Yes\n'
                   'key3: false\n'
                   'key4: no\n'
                   'key5: yes\n',
                   conf)

    def test_no_allowed_values(self):
        conf = ('truthy:\n'
                '  allowed-values: []\n')
        self.check('---\n'
                   'key1: foo\n'
                   'key2: bar\n', conf)
        self.check('---\n'
                   'key1: true\n'
                   'key2: yes\n'
                   'key3: false\n'
                   'key4: no\n', conf,
                   problem1=(2, 7), problem2=(3, 7),
                   problem3=(4, 7), problem4=(5, 7))
        self.check('%YAML 1.1\n'
                   '---\n'
                   'key1: true\n'
                   'key2: yes\n'
                   'key3: false\n'
                   'key4: no\n', conf,
                   problem1=(3, 7), problem2=(4, 7),
                   problem3=(5, 7), problem4=(6, 7))
        self.check('%YAML 1.2\n'
                   '---\n'
                   'key1: true\n'
                   'key2: yes\n'
                   'key3: false\n'
                   'key4: no\n', conf,
                   problem1=(3, 7), problem2=(5, 7))

    def test_explicit_types(self):
        conf = 'truthy: enable\n'
        self.check('---\n'
                   'string1: !!str True\n'
                   'string2: !!str yes\n'
                   'string3: !!str off\n'
                   'encoded: !!binary |\n'
                   '           True\n'
                   '           OFF\n'
                   '           pad==\n'  # this decodes as 'N\xbb\x9e8Qii'
                   'boolean1: !!bool true\n'
                   'boolean2: !!bool "false"\n'
                   'boolean3: !!bool FALSE\n'
                   'boolean4: !!bool True\n'
                   'boolean5: !!bool off\n'
                   'boolean6: !!bool NO\n',
                   conf)

    def test_check_keys_disabled(self):
        conf = ('truthy:\n'
                '  allowed-values: []\n'
                '  check-keys: false\n'
                'key-duplicates: disable\n')
        self.check('---\n'
                   'YES: 0\n'
                   'Yes: 0\n'
                   'yes: 0\n'
                   'No: 0\n'
                   'No: 0\n'
                   'no: 0\n'
                   'TRUE: 0\n'
                   'True: 0\n'
                   'true: 0\n'
                   'FALSE: 0\n'
                   'False: 0\n'
                   'false: 0\n'
                   'ON: 0\n'
                   'On: 0\n'
                   'on: 0\n'
                   'OFF: 0\n'
                   'Off: 0\n'
                   'off: 0\n'
                   'YES:\n'
                   '  Yes:\n'
                   '    yes:\n'
                   '      on: 0\n',
                   conf)
