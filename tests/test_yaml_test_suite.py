# Copyright (C) 2026 Kushal Dave
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

"""Crash regression coverage from the optional, pinned YAML Test Suite."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

from yamllint import config, linter

CORPUS = Path(__file__).with_name('yaml-test-suite')
SETUP = 'git submodule update --init tests/yaml-test-suite'
# Exercise optional rules too, without turning diagnostics into failures.
CONFIG = config.YamlLintConfig('''
extends: default
rules:
  document-end: enable
  empty-values: enable
  float-values: enable
  key-ordering: enable
  octal-values: enable
  quoted-strings: enable
''')
# A different exception or an unexpected pass fails, prompting baseline review.
# 4H7K: key-ordering stack underflow on an unmatched closing flow token.
# https://github.com/adrienverge/yamllint/pull/829
KNOWN_FAILURES = {'4H7K': (IndexError, '^pop from empty list$')}


def corpus_suite(root, required=False):
    """Build individually reported tests, including numbered subcases."""
    suite = unittest.TestSuite()
    paths = sorted(root.rglob('in.yaml'))
    if not paths:
        def missing():
            message = f'YAML Test Suite missing or empty; run: {SETUP}'
            if required:
                raise AssertionError(message)
            raise unittest.SkipTest(message)
        suite.addTest(unittest.FunctionTestCase(missing))
    else:
        for path in paths:
            case_id = path.parent.relative_to(root).as_posix()
            suite.addTest(CorpusCase(path, case_id))
    return suite


class CorpusCase(unittest.TestCase):
    def __init__(self, path='runTest', case_id=None):
        super().__init__()
        self.path = path
        self.case_id = case_id

    def id(self):
        return f'{__name__}.{self.case_id}'

    def __str__(self):
        kind = 'invalid' if self.path.with_name('error').exists() else 'valid'
        return f'{self.id()} ({kind})'

    def runTest(self):
        # Byte input preserves BOMs/newlines and uses yamllint's own decoder.
        # Materialize the lazy generator: creating it alone checks nothing.
        if self.case_id in KNOWN_FAILURES:
            exception, message = KNOWN_FAILURES[self.case_id]
            with self.assertRaisesRegex(exception, message):
                list(linter.run(self.path.read_bytes(), CONFIG))
        else:
            list(linter.run(self.path.read_bytes(), CONFIG))


class HarnessTestCase(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write_case(self, case_id, text='--- value\n', invalid=False):
        path = self.root / case_id / 'in.yaml'
        path.parent.mkdir(parents=True)
        path.write_text(text, encoding='utf-8')
        if invalid:
            path.with_name('error').touch()
        return path

    def run_suite(self, required=False):
        result = unittest.TestResult()
        corpus_suite(self.root, required).run(result)
        return result

    def test_optional_missing_corpus_is_visible(self):
        result = self.run_suite()
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(len(result.skipped), 1)
        self.assertIn(SETUP, result.skipped[0][1])

    def test_required_empty_corpus_fails(self):
        result = self.run_suite(required=True)
        self.assertEqual(len(result.failures), 1)
        self.assertFalse(result.skipped)

    def test_nested_cases_and_diagnostics(self):
        self.write_case('AAAA')
        self.write_case('BBBB/00', '[\n', invalid=True)
        self.write_case('BBBB/01', 'foo: bar  \n')
        suite = corpus_suite(self.root)
        self.assertEqual([case.case_id for case in suite],
                         ['AAAA', 'BBBB/00', 'BBBB/01'])
        result = self.run_suite()
        self.assertEqual(result.testsRun, 3)
        self.assertTrue(result.wasSuccessful())
        self.assertFalse(result.skipped)

    def test_generator_exception_is_a_case_error(self):
        self.write_case('AAAA')

        def crashing_runner(*args):
            yield linter.LintProblem(1, 1)
            raise RuntimeError('injected crash')
        with mock.patch.object(linter, 'run', crashing_runner):
            result = self.run_suite()
        self.assertEqual(len(result.errors), 1)
        self.assertIn('AAAA', result.errors[0][0].id())
        self.assertIn('injected crash', result.errors[0][1])

    def test_known_failure_must_still_fail_as_documented(self):
        self.write_case('4H7K')
        with mock.patch.object(linter, 'run', return_value=iter(())):
            self.assertEqual(len(self.run_suite().failures), 1)
        with mock.patch.object(linter, 'run', side_effect=ValueError('new')):
            self.assertEqual(len(self.run_suite().errors), 1)
        with mock.patch.object(linter, 'run',
                               side_effect=IndexError('different')):
            self.assertEqual(len(self.run_suite().failures), 1)
        with mock.patch.object(linter, 'run',
                               side_effect=IndexError('pop from empty list')):
            self.assertTrue(self.run_suite().wasSuccessful())


def load_tests(loader, tests, pattern):
    # Replace discovery's placeholder CorpusCase with the actual fixtures.
    suite = loader.loadTestsFromTestCase(HarnessTestCase)
    suite.addTests(corpus_suite(CORPUS))
    return suite


if __name__ == '__main__':
    # This CI entry point must fail when the submodule was not initialized.
    result = unittest.TextTestRunner(verbosity=2).run(
        corpus_suite(CORPUS, required=True))
    raise SystemExit(not result.wasSuccessful())
