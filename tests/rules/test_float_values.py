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
        conf = (
            'float-values: disable\n'
            'new-line-at-end-of-file: disable\n'
            'document-start: disable\n'
        )
        self.check('angle: 0.0', conf)
        self.check('angle: .NaN', conf)
        self.check('angle: .INF', conf)
        self.check('angle: .1', conf)
        self.check('angle: 10e-6', conf)
        self.check(
            '- &angle .0\n'
            '- *angle\n',
            conf,
        )
        self.check(
            '- &angle 10e6\n'
            '- *angle\n',
            conf,
        )
        self.check(
            '- &angle .nan\n'
            '- *angle\n',
            conf,
        )
        self.check(
            '- &angle .inf\n'
            '- *angle\n',
            conf,
        )

    def test_numeral_before_decimal(self):
        conf = (
            'float-values:\n'
            '  require-numeral-before-decimal: true\n'
            '  forbid-scientific-notation: false\n'
            '  forbid-nan: false\n'
            '  forbid-inf: false\n'
            'new-line-at-end-of-file: disable\n'
            'document-start: disable\n'
        )
        self.check('angle: .1', conf, problem=(1, 8))
        self.check('angle: 0.0', conf)
        self.check('angle: \'.1\'', conf)
        self.check('angle: !custom_tag 0.0', conf)
        self.check(
            '- &angle 0.0\n'
            '- *angle\n',
            conf
        )
        self.check(
            '- &angle .0\n'
            '- *angle\n',
            conf,
            problem=(1, 10)
        )

    def test_scientific_notation(self):
        conf = (
            'float-values:\n'
            '  require-numeral-before-decimal: false\n'
            '  forbid-scientific-notation: true\n'
            '  forbid-nan: false\n'
            '  forbid-inf: false\n'
            'new-line-at-end-of-file: disable\n'
            'document-start: disable\n'
        )
        self.check('angle: 10e6', conf, problem=(1, 8))
        self.check('angle: 10e-6', conf, problem=(1, 8))
        self.check('angle: 0.00001', conf)
        self.check('angle: \'10e-6\'', conf)
        self.check('angle: !custom_tag 10e-6', conf)
        self.check(
            '- &angle 0.000001\n'
            '- *angle\n',
            conf
        )
        self.check(
            '- &angle 10e-6\n'
            '- *angle\n',
            conf,
            problem=(1, 10)
        )
        self.check(
            '- &angle 10e6\n'
            '- *angle\n',
            conf,
            problem=(1, 10)
        )

    def test_nan(self):
        conf = (
            'float-values:\n'
            '  require-numeral-before-decimal: false\n'
            '  forbid-scientific-notation: false\n'
            '  forbid-nan: true\n'
            '  forbid-inf: false\n'
            'new-line-at-end-of-file: disable\n'
            'document-start: disable\n'
        )
        self.check('angle: .NaN', conf, problem=(1, 8))
        self.check('angle: .NAN', conf, problem=(1, 8))
        self.check('angle: \'.NaN\'', conf)
        self.check('angle: !custom_tag .NaN', conf)
        self.check(
            '- &angle .nan\n'
            '- *angle\n',
            conf,
            problem=(1, 10)
        )

    def test_inf(self):
        conf = (
            'float-values:\n'
            '  require-numeral-before-decimal: false\n'
            '  forbid-scientific-notation: false\n'
            '  forbid-nan: false\n'
            '  forbid-inf: true\n'
            'new-line-at-end-of-file: disable\n'
            'document-start: disable\n'
        )
        self.check('angle: .inf', conf, problem=(1, 8))
        self.check('angle: .INF', conf, problem=(1, 8))
        self.check('angle: -.inf', conf, problem=(1, 8))
        self.check('angle: -.INF', conf, problem=(1, 8))
        self.check('angle: \'.inf\'', conf)
        self.check('angle: !custom_tag .inf', conf)
        self.check(
            '- &angle .inf\n'
            '- *angle\n',
            conf,
            problem=(1, 10)
        )
        self.check(
            '- &angle -.inf\n'
            '- *angle\n',
            conf,
            problem=(1, 10)
        )
