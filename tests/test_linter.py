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

import io
import unittest

from yamllint import linter
from yamllint.config import YamlLintConfig


class LinterTestCase(unittest.TestCase):
    def fake_config(self):
        return YamlLintConfig('extends: default')

    def test_run_on_string(self):
        linter.run('test: document', self.fake_config())

    def test_run_on_bytes(self):
        linter.run(b'test: document', self.fake_config())

    def test_run_on_unicode(self):
        linter.run('test: document', self.fake_config())

    def test_run_on_stream(self):
        linter.run(io.StringIO('hello'), self.fake_config())

    def test_run_on_int(self):
        self.assertRaises(TypeError, linter.run, 42, self.fake_config())

    def test_run_on_list(self):
        self.assertRaises(TypeError, linter.run,
                          ['h', 'e', 'l', 'l', 'o'], self.fake_config())

    def test_run_on_non_ascii_chars(self):
        s = ('- hétérogénéité\n'
             '# 19.99 €\n')
        linter.run(s, self.fake_config())
        linter.run(s.encode('utf-8'), self.fake_config())
        linter.run(s.encode('iso-8859-15'), self.fake_config())

        s = ('- お早う御座います。\n'
             '# الأَبْجَدِيَّة العَرَبِيَّة\n')
        linter.run(s, self.fake_config())
        linter.run(s.encode('utf-8'), self.fake_config())

    def test_linter_problem_repr_without_rule(self):
        problem = linter.LintProblem(1, 2, 'problem')

        self.assertEqual(str(problem), '1:2: problem')

    def test_linter_problem_repr_with_rule(self):
        problem = linter.LintProblem(1, 2, 'problem', 'rule-id')

        self.assertEqual(str(problem), '1:2: problem (rule-id)')
