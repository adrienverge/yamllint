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
from tests.rules.test_truthy import TruthyTestCase


class KeyScalarTypesTestCase(RuleTestCase):
    rule_id = 'key-scalar-types'

    def _check_all(self, target, conf, passes):
        """
        Expect all the lines in the target to pass, or all to fail, depending
        on the value of `passes`.
        """
        lines = target.splitlines()[1:]
        if passes:
            problems = {}
        else:
            problems = {
                f"problem{n + 1}": (n + 2, len(line) - len(line.strip()) + 1)
                for n, line in enumerate(lines)
            }
        self.check(target, conf, **problems)

    def _check_scalar_string_types(self, conf, passes: bool):
        self._check_all('---\n'
                        'foo: string\n'
                        '"true": string\n'
                        '"234": string\n'
                        '\'345\': string\n'
                        '!!str 456: string\n'
                        'a123: string\n'
                        '"010": string\n'
                        '"0.0": string\n'
                        'v1.23: string\n'
                        '"2023-10-11": string\n'
                        '"null": string\n'
                        'nulL: string\n'
                        'b{}: string\n'
                        'c[]: string\n'
                        # These may look like ints or floats, but aren't ...
                        '08: string\n'  # invalid octal integer
                        '+.0: string\n'  # invalid float
                        '-.0: string\n'  # invalid float
                        '-0e0: string\n'  # invalid float
                        '0e-0: string\n'  # invalid float
                        '-0e-0: string\n'  # invalid float
                        '+0e-0: string\n'  # invalid float
                        # These may look like timestamps, but aren't ...
                        '2023-10-11 12:13: string\n'  # missing seconds
                        '2023-10-11-12:13:14: string\n'  # wrong separator
                        '2023-10-11T12:13:14,59: string\n',  # decimal comma
                        conf, passes)

        # The strings in the check above were all in column 1. Now check some
        # strings that are in column 2 or later.
        level_n_strings = (
            '---\n'
            '? foo: string1\n'  # key string at column 3
            ': string key in block mapping key\n'
            '? - foo: string2\n'  # key string at column 5
            ': string key in mapping in block sequence key\n'
            '{foo: string3}: string key in flow mapping key\n'  # column 2
            '[foo: string4]: string key in mapping in flow sequence key\n'  # 2
        )
        if passes:
            problems = {}
        else:
            problems = {
                "problem1": (2, 3),
                "problem2": (4, 5),
                "problem3": (6, 2),
                "problem4": (7, 2)
            }
        self.check(level_n_strings, conf, **problems)

    def _check_scalar_int_types(self, conf, passes: bool):
        self._check_all('---\n'
                        '0: integer\n'
                        '00: integer\n'
                        '010: integer\n'
                        '123: integer\n',
                        conf, passes)

    def _check_scalar_float_types(self, conf, passes: bool):
        self._check_all('---\n'
                        '0.0: float\n'
                        '00.00: float\n'
                        '.0: float\n'
                        '0.: float\n'
                        '+0.0: float\n'
                        '+00.00: float\n'
                        '+0.: float\n'
                        '-0.0: float\n'
                        '-00.00: float\n'
                        '-0.: float\n'
                        '.123: float\n'
                        '1.23: float\n'
                        '1.e+0: float\n'
                        '1.e+2: float\n'
                        '1.e+02: float\n'
                        '1.0e+02: float\n'
                        '.inf: float\n'
                        '+.inf: float\n'
                        '-.inf: float\n'
                        '.nan: float\n',
                        conf, passes)

    def _check_scalar_bool_types(self, conf, passes: bool):
        # Use test case data from truthy
        conf = f'{conf}\n{TruthyTestCase.TRUTHY_CONF_DISABLED}'
        self._check_all(TruthyTestCase.TRUTHY_KEYS, conf, passes)

    def _check_scalar_null_types(self, conf, passes: bool):
        self._check_all('---\n'
                        'null: "null"\n'
                        'Null: "null"\n'
                        'NULL: "null"\n'
                        '!!null null: "null"\n',
                        conf, passes)

    def _check_scalar_timestamp_types(self, conf, passes: bool):
        self._check_all('---\n'
                        '2023-10-11: timestamp\n'
                        '2023-10-11 12:34:56: timestamp\n'
                        '2023-10-11T12:34:56: timestamp\n'
                        '2023-10-11t12:34:56: timestamp\n'
                        '2023-10-11 12:34:56.789: timestamp\n',
                        conf, passes)

    def _check_all_scalar_types(self, conf):
        self._check_scalar_string_types(conf, passes=True)
        self._check_scalar_int_types(conf, passes=True)
        self._check_scalar_float_types(conf, passes=True)
        self._check_scalar_bool_types(conf, passes=True)
        self._check_scalar_null_types(conf, passes=True)
        self._check_scalar_timestamp_types(conf, passes=True)

    def test_disabled(self):
        conf = 'key-scalar-types: disable'

        self._check_all_scalar_types(conf)

    def test_default(self):
        conf = 'key-scalar-types: {}'

        self._check_all_scalar_types(conf)

    def test_str(self):
        conf = 'key-scalar-types: {allowed: [str]}'
        self._check_scalar_string_types(conf, passes=True)
        self._check_scalar_int_types(conf, passes=False)
        self._check_scalar_float_types(conf, passes=False)
        self._check_scalar_bool_types(conf, passes=False)
        self._check_scalar_null_types(conf, passes=False)
        self._check_scalar_timestamp_types(conf, passes=False)

    def test_int(self):
        conf = 'key-scalar-types: {allowed: [int]}'
        self._check_scalar_string_types(conf, passes=False)
        self._check_scalar_int_types(conf, passes=True)
        self._check_scalar_float_types(conf, passes=False)
        self._check_scalar_bool_types(conf, passes=False)
        self._check_scalar_null_types(conf, passes=False)
        self._check_scalar_timestamp_types(conf, passes=False)

    def test_float(self):
        conf = 'key-scalar-types: {allowed: [float]}'
        self._check_scalar_string_types(conf, passes=False)
        self._check_scalar_int_types(conf, passes=False)
        self._check_scalar_float_types(conf, passes=True)
        self._check_scalar_bool_types(conf, passes=False)
        self._check_scalar_null_types(conf, passes=False)
        self._check_scalar_timestamp_types(conf, passes=False)

    def test_bool(self):
        conf = 'key-scalar-types: {allowed: [bool]}'
        self._check_scalar_string_types(conf, passes=False)
        self._check_scalar_int_types(conf, passes=False)
        self._check_scalar_float_types(conf, passes=False)
        self._check_scalar_bool_types(conf, passes=True)
        self._check_scalar_null_types(conf, passes=False)
        self._check_scalar_timestamp_types(conf, passes=False)

    def test_null(self):
        conf = 'key-scalar-types: {allowed: ["null"]}'
        self._check_scalar_string_types(conf, passes=False)
        self._check_scalar_int_types(conf, passes=False)
        self._check_scalar_float_types(conf, passes=False)
        self._check_scalar_bool_types(conf, passes=False)
        self._check_scalar_null_types(conf, passes=True)
        self._check_scalar_timestamp_types(conf, passes=False)

    def test_timestamp(self):
        conf = 'key-scalar-types: {allowed: [timestamp]}'
        self._check_scalar_string_types(conf, passes=False)
        self._check_scalar_int_types(conf, passes=False)
        self._check_scalar_float_types(conf, passes=False)
        self._check_scalar_bool_types(conf, passes=False)
        self._check_scalar_null_types(conf, passes=False)
        self._check_scalar_timestamp_types(conf, passes=True)
