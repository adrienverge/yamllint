# Copyright (C) 2023 Henry Gessau
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


class KeyNodeKindsTestCase(RuleTestCase):
    rule_id = 'key-node-kinds'

    def test_disabled(self):
        conf = 'key-node-kinds: disable'

        self.check('---\n'
                   '{foo: bar}: mapping\n'
                   '[foo, bar]: sequence\n'
                   'foo: str\n'
                   '123: int\n'
                   '1.23: float\n'
                   'true: bool\n'
                   'null: "null"\n'
                   '2023-10-11: timestamp\n',
                   conf)

    def test_default(self):
        conf = 'key-node-kinds: {}'

        self.check('---\n'
                   '{foo: bar}: mapping\n'      # fails
                   '[foo, bar]: sequence\n'     # fails
                   'foo: str\n'
                   '123: int\n'
                   '1.23: float\n'
                   'true: bool\n'
                   'null: "null"\n'
                   '2023-10-11: timestamp\n',
                   conf,
                   problem1=(2, 1), problem2=(3, 1))

    def test_allow_mapping(self):
        conf = 'key-node-kinds:\n'\
               '  allow-mapping: true'

        self.check('---\n'
                   'true: boolean\n'
                   '123: integer\n'
                   '1.23: floating point number\n'
                   'foo: string1\n'
                   '"234": string2\n'
                   '\'345\': string3\n'
                   '!!str 456: string4\n'
                   '2023-10-11: timestamp\n'
                   'null: "null"\n'
                   '? foo: string\n'
                   ': block mapping\n'
                   '{foo: string}: flow mapping\n'
                   '{}: empty mapping\n'
                   '? - foo\n'                              # fails
                   ': block sequence\n'
                   '[foo]: flow sequence\n'                 # fails
                   '[foo: string]: mapping in sequence\n'   # fails
                   '{[foo]: bar}: sequence in mapping\n'    # fails
                   '[]: empty sequence\n',                  # fails
                   conf,
                   problem1=(15, 3), problem2=(17, 1), problem3=(18, 1),
                   problem4=(19, 2), problem5=(20, 1))

    def test_allow_sequence(self):
        conf = 'key-node-kinds:\n'\
               '  allow-sequence: true'

        self.check('---\n'
                   'true: boolean\n'
                   '123: integer\n'
                   '1.23: floating point number\n'
                   'foo: string1\n'
                   '"234": string2\n'
                   '\'345\': string3\n'
                   '!!str 456: string4\n'
                   '2023-10-11: timestamp\n'
                   'null: "null"\n'
                   '? foo: string\n'                        # fails
                   ': block mapping\n'
                   '{foo: string}: flow mapping\n'          # fails
                   '{}: empty mapping\n'                    # fails
                   '? - foo\n'
                   ': block sequence\n'
                   '[foo]: flow sequence\n'
                   '[foo: string]: mapping in sequence\n'
                   '[]: empty sequence\n',
                   conf,
                   problem1=(11, 3), problem2=(13, 1), problem3=(14, 1))

    def test_forbid_scalar(self):
        conf = 'key-node-kinds:\n'\
               '  allow-mapping: true\n'\
               '  allow-sequence: true\n'\
               '  allow-scalar: false'

        self.check('---\n'
                   'true: boolean\n'                        # fails
                   '123: integer\n'                         # fails
                   '1.23: floating point number\n'          # fails
                   'foo: string1\n'                         # fails
                   '"234": string2\n'                       # fails
                   '\'345\': string3\n'                     # fails
                   '!!str 456: string4\n'                   # fails
                   '2023-10-11: timestamp\n'                # fails
                   'null: "null"\n'                         # fails
                   '? [foo]: sequence\n'
                   ': block mapping\n'
                   '{[foo]: sequence}: flow mapping\n'
                   '{}: empty mapping\n'
                   '? - foo\n'
                   ': block sequence\n'
                   '[foo]: flow sequence\n'
                   '[foo: string]: mapping in sequence\n'   # fails
                   '{[foo]: bar}: sequence in mapping\n'
                   '[]: empty sequence\n',
                   conf,
                   problem1=(2, 1), problem2=(3, 1), problem3=(4, 1),
                   problem4=(5, 1), problem5=(6, 1), problem6=(7, 1),
                   problem7=(8, 1), problem8=(9, 1), problem9=(10, 1),
                   problem10=(18, 2))
