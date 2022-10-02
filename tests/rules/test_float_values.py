# Copyright (C) 2022 the yamllint contributors
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


class FloatValuesTestCase(RuleTestCase):
    rule_id = 'float-values'

    def test_disabled(self):
        conf = 'float-values: disable\n'
        self.check('---\n'
                   '- 0.0\n'
                   '- .NaN\n'
                   '- .INF\n'
                   '- .1\n'
                   '- 10e-6\n',
                   conf)

    def test_numeral_before_decimal(self):
        conf = (
            'float-values:\n'
            '  require-numeral-before-decimal: true\n'
            '  forbid-scientific-notation: false\n'
            '  forbid-nan: false\n'
            '  forbid-inf: false\n')
        self.check('---\n'
                   '- 0.0\n'
                   '- .1\n'
                   '- \'.1\'\n'
                   '- string.1\n'
                   '- .1string\n'
                   '- !custom_tag .2\n'
                   '- &angle1 0.0\n'
                   '- *angle1\n'
                   '- &angle2 .3\n'
                   '- *angle2\n',
                   conf,
                   problem1=(3, 3),
                   problem2=(10, 11))

    def test_scientific_notation(self):
        conf = (
            'float-values:\n'
            '  require-numeral-before-decimal: false\n'
            '  forbid-scientific-notation: true\n'
            '  forbid-nan: false\n'
            '  forbid-inf: false\n')
        self.check('---\n'
                   '- 10e6\n'
                   '- 10e-6\n'
                   '- 0.00001\n'
                   '- \'10e-6\'\n'
                   '- string10e-6\n'
                   '- 10e-6string\n'
                   '- !custom_tag 10e-6\n'
                   '- &angle1 0.000001\n'
                   '- *angle1\n'
                   '- &angle2 10e-6\n'
                   '- *angle2\n'
                   '- &angle3 10e6\n'
                   '- *angle3\n',
                   conf,
                   problem1=(2, 3),
                   problem2=(3, 3),
                   problem3=(11, 11),
                   problem4=(13, 11))

    def test_nan(self):
        conf = (
            'float-values:\n'
            '  require-numeral-before-decimal: false\n'
            '  forbid-scientific-notation: false\n'
            '  forbid-nan: true\n'
            '  forbid-inf: false\n')
        self.check('---\n'
                   '- .NaN\n'
                   '- .NAN\n'
                   '- \'.NaN\'\n'
                   '- a.NaN\n'
                   '- .NaNa\n'
                   '- !custom_tag .NaN\n'
                   '- &angle .nan\n'
                   '- *angle\n',
                   conf,
                   problem1=(2, 3),
                   problem2=(3, 3),
                   problem3=(8, 10))

    def test_inf(self):
        conf = (
            'float-values:\n'
            '  require-numeral-before-decimal: false\n'
            '  forbid-scientific-notation: false\n'
            '  forbid-nan: false\n'
            '  forbid-inf: true\n')
        self.check('---\n'
                   '- .inf\n'
                   '- .INF\n'
                   '- -.inf\n'
                   '- -.INF\n'
                   '- \'.inf\'\n'
                   '- ∞.infinity\n'
                   '- .infinity∞\n'
                   '- !custom_tag .inf\n'
                   '- &angle .inf\n'
                   '- *angle\n'
                   '- &angle -.inf\n'
                   '- *angle\n',
                   conf,
                   problem1=(2, 3),
                   problem2=(3, 3),
                   problem3=(4, 3),
                   problem4=(5, 3),
                   problem5=(10, 10),
                   problem6=(12, 10))
