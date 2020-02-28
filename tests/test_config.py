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

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import os
import shutil
import sys
import tempfile
import unittest

from tests.common import build_temp_workspace

from yamllint import cli
from yamllint import config


class SimpleConfigTestCase(unittest.TestCase):
    def test_parse_config(self):
        new = config.YamlLintConfig('rules:\n'
                                    '  colons:\n'
                                    '    max-spaces-before: 0\n'
                                    '    max-spaces-after: 1\n')

        self.assertEqual(list(new.rules.keys()), ['colons'])
        self.assertEqual(new.rules['colons']['max-spaces-before'], 0)
        self.assertEqual(new.rules['colons']['max-spaces-after'], 1)

        self.assertEqual(len(new.enabled_rules(None)), 1)

    def test_invalid_conf(self):
        with self.assertRaises(config.YamlLintConfigError):
            config.YamlLintConfig('not: valid: yaml')

    def test_unknown_rule(self):
        with self.assertRaisesRegexp(
                config.YamlLintConfigError,
                'invalid config: no such rule: "this-one-does-not-exist"'):
            config.YamlLintConfig('rules:\n'
                                  '  this-one-does-not-exist: enable\n')

    def test_missing_option(self):
        c = config.YamlLintConfig('rules:\n'
                                  '  colons: enable\n')
        self.assertEqual(c.rules['colons']['max-spaces-before'], 0)
        self.assertEqual(c.rules['colons']['max-spaces-after'], 1)

        c = config.YamlLintConfig('rules:\n'
                                  '  colons:\n'
                                  '    max-spaces-before: 9\n')
        self.assertEqual(c.rules['colons']['max-spaces-before'], 9)
        self.assertEqual(c.rules['colons']['max-spaces-after'], 1)

    def test_unknown_option(self):
        with self.assertRaisesRegexp(
                config.YamlLintConfigError,
                'invalid config: unknown option "abcdef" for rule "colons"'):
            config.YamlLintConfig('rules:\n'
                                  '  colons:\n'
                                  '    max-spaces-before: 0\n'
                                  '    max-spaces-after: 1\n'
                                  '    abcdef: yes\n')

    def test_yes_no_for_booleans(self):
        c = config.YamlLintConfig('rules:\n'
                                  '  indentation:\n'
                                  '    spaces: 2\n'
                                  '    indent-sequences: true\n'
                                  '    check-multi-line-strings: false\n')
        self.assertTrue(c.rules['indentation']['indent-sequences'])
        self.assertEqual(c.rules['indentation']['check-multi-line-strings'],
                         False)

        c = config.YamlLintConfig('rules:\n'
                                  '  indentation:\n'
                                  '    spaces: 2\n'
                                  '    indent-sequences: yes\n'
                                  '    check-multi-line-strings: false\n')
        self.assertTrue(c.rules['indentation']['indent-sequences'])
        self.assertEqual(c.rules['indentation']['check-multi-line-strings'],
                         False)

        c = config.YamlLintConfig('rules:\n'
                                  '  indentation:\n'
                                  '    spaces: 2\n'
                                  '    indent-sequences: whatever\n'
                                  '    check-multi-line-strings: false\n')
        self.assertEqual(c.rules['indentation']['indent-sequences'],
                         'whatever')
        self.assertEqual(c.rules['indentation']['check-multi-line-strings'],
                         False)

        with self.assertRaisesRegexp(
                config.YamlLintConfigError,
                'invalid config: option "indent-sequences" of "indentation" '
                'should be in '):
            c = config.YamlLintConfig('rules:\n'
                                      '  indentation:\n'
                                      '    spaces: 2\n'
                                      '    indent-sequences: YES!\n'
                                      '    check-multi-line-strings: false\n')

    def test_enable_disable_keywords(self):
        c = config.YamlLintConfig('rules:\n'
                                  '  colons: enable\n'
                                  '  hyphens: disable\n')
        self.assertEqual(c.rules['colons'], {'level': 'error',
                                             'max-spaces-after': 1,
                                             'max-spaces-before': 0})
        self.assertEqual(c.rules['hyphens'], False)

    def test_validate_rule_conf(self):
        class Rule(object):
            ID = 'fake'

        self.assertFalse(config.validate_rule_conf(Rule, False))
        self.assertEqual(config.validate_rule_conf(Rule, {}),
                         {'level': 'error'})

        config.validate_rule_conf(Rule, {'level': 'error'})
        config.validate_rule_conf(Rule, {'level': 'warning'})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule, {'level': 'warn'})

        Rule.CONF = {'length': int}
        Rule.DEFAULT = {'length': 80}
        config.validate_rule_conf(Rule, {'length': 8})
        config.validate_rule_conf(Rule, {})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule, {'height': 8})

        Rule.CONF = {'a': bool, 'b': int}
        Rule.DEFAULT = {'a': True, 'b': -42}
        config.validate_rule_conf(Rule, {'a': True, 'b': 0})
        config.validate_rule_conf(Rule, {'a': True})
        config.validate_rule_conf(Rule, {'b': 0})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule, {'a': 1, 'b': 0})

        Rule.CONF = {'choice': (True, 88, 'str')}
        Rule.DEFAULT = {'choice': 88}
        config.validate_rule_conf(Rule, {'choice': True})
        config.validate_rule_conf(Rule, {'choice': 88})
        config.validate_rule_conf(Rule, {'choice': 'str'})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule, {'choice': False})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule, {'choice': 99})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule, {'choice': 'abc'})

        Rule.CONF = {'choice': (int, 'hardcoded')}
        Rule.DEFAULT = {'choice': 1337}
        config.validate_rule_conf(Rule, {'choice': 42})
        config.validate_rule_conf(Rule, {'choice': 'hardcoded'})
        config.validate_rule_conf(Rule, {})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule, {'choice': False})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule, {'choice': 'abc'})

        Rule.CONF = {'multiple': ['item1', 'item2', 'item3']}
        Rule.DEFAULT = {'multiple': ['item1']}
        config.validate_rule_conf(Rule, {'multiple': []})
        config.validate_rule_conf(Rule, {'multiple': ['item2']})
        config.validate_rule_conf(Rule, {'multiple': ['item2', 'item3']})
        config.validate_rule_conf(Rule, {})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule,
                          {'multiple': 'item1'})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule,
                          {'multiple': ['']})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule,
                          {'multiple': ['item1', 4]})
        self.assertRaises(config.YamlLintConfigError,
                          config.validate_rule_conf, Rule,
                          {'multiple': ['item4']})


class ExtendedConfigTestCase(unittest.TestCase):
    def test_extend_on_object(self):
        old = config.YamlLintConfig('rules:\n'
                                    '  colons:\n'
                                    '    max-spaces-before: 0\n'
                                    '    max-spaces-after: 1\n')
        new = config.YamlLintConfig('rules:\n'
                                    '  hyphens:\n'
                                    '    max-spaces-after: 2\n')
        new.extend(old)

        self.assertEqual(sorted(new.rules.keys()), ['colons', 'hyphens'])
        self.assertEqual(new.rules['colons']['max-spaces-before'], 0)
        self.assertEqual(new.rules['colons']['max-spaces-after'], 1)
        self.assertEqual(new.rules['hyphens']['max-spaces-after'], 2)

        self.assertEqual(len(new.enabled_rules(None)), 2)

    def test_extend_on_file(self):
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('rules:\n'
                    '  colons:\n'
                    '    max-spaces-before: 0\n'
                    '    max-spaces-after: 1\n')
            f.flush()
            c = config.YamlLintConfig('extends: ' + f.name + '\n'
                                      'rules:\n'
                                      '  hyphens:\n'
                                      '    max-spaces-after: 2\n')

        self.assertEqual(sorted(c.rules.keys()), ['colons', 'hyphens'])
        self.assertEqual(c.rules['colons']['max-spaces-before'], 0)
        self.assertEqual(c.rules['colons']['max-spaces-after'], 1)
        self.assertEqual(c.rules['hyphens']['max-spaces-after'], 2)

        self.assertEqual(len(c.enabled_rules(None)), 2)

    def test_extend_remove_rule(self):
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('rules:\n'
                    '  colons:\n'
                    '    max-spaces-before: 0\n'
                    '    max-spaces-after: 1\n'
                    '  hyphens:\n'
                    '    max-spaces-after: 2\n')
            f.flush()
            c = config.YamlLintConfig('extends: ' + f.name + '\n'
                                      'rules:\n'
                                      '  colons: disable\n')

        self.assertEqual(sorted(c.rules.keys()), ['colons', 'hyphens'])
        self.assertFalse(c.rules['colons'])
        self.assertEqual(c.rules['hyphens']['max-spaces-after'], 2)

        self.assertEqual(len(c.enabled_rules(None)), 1)

    def test_extend_edit_rule(self):
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('rules:\n'
                    '  colons:\n'
                    '    max-spaces-before: 0\n'
                    '    max-spaces-after: 1\n'
                    '  hyphens:\n'
                    '    max-spaces-after: 2\n')
            f.flush()
            c = config.YamlLintConfig('extends: ' + f.name + '\n'
                                      'rules:\n'
                                      '  colons:\n'
                                      '    max-spaces-before: 3\n'
                                      '    max-spaces-after: 4\n')

        self.assertEqual(sorted(c.rules.keys()), ['colons', 'hyphens'])
        self.assertEqual(c.rules['colons']['max-spaces-before'], 3)
        self.assertEqual(c.rules['colons']['max-spaces-after'], 4)
        self.assertEqual(c.rules['hyphens']['max-spaces-after'], 2)

        self.assertEqual(len(c.enabled_rules(None)), 2)

    def test_extend_reenable_rule(self):
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('rules:\n'
                    '  colons:\n'
                    '    max-spaces-before: 0\n'
                    '    max-spaces-after: 1\n'
                    '  hyphens: disable\n')
            f.flush()
            c = config.YamlLintConfig('extends: ' + f.name + '\n'
                                      'rules:\n'
                                      '  hyphens:\n'
                                      '    max-spaces-after: 2\n')

        self.assertEqual(sorted(c.rules.keys()), ['colons', 'hyphens'])
        self.assertEqual(c.rules['colons']['max-spaces-before'], 0)
        self.assertEqual(c.rules['colons']['max-spaces-after'], 1)
        self.assertEqual(c.rules['hyphens']['max-spaces-after'], 2)

        self.assertEqual(len(c.enabled_rules(None)), 2)

    def test_extend_recursive_default_values(self):
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('rules:\n'
                    '  braces:\n'
                    '    max-spaces-inside: 1248\n')
            f.flush()
            c = config.YamlLintConfig('extends: ' + f.name + '\n'
                                      'rules:\n'
                                      '  braces:\n'
                                      '    min-spaces-inside-empty: 2357\n')

        self.assertEqual(c.rules['braces']['min-spaces-inside'], 0)
        self.assertEqual(c.rules['braces']['max-spaces-inside'], 1248)
        self.assertEqual(c.rules['braces']['min-spaces-inside-empty'], 2357)
        self.assertEqual(c.rules['braces']['max-spaces-inside-empty'], -1)

        with tempfile.NamedTemporaryFile('w') as f:
            f.write('rules:\n'
                    '  colons:\n'
                    '    max-spaces-before: 1337\n')
            f.flush()
            c = config.YamlLintConfig('extends: ' + f.name + '\n'
                                      'rules:\n'
                                      '  colons: enable\n')

        self.assertEqual(c.rules['colons']['max-spaces-before'], 1337)
        self.assertEqual(c.rules['colons']['max-spaces-after'], 1)

        with tempfile.NamedTemporaryFile('w') as f1, \
                tempfile.NamedTemporaryFile('w') as f2:
            f1.write('rules:\n'
                     '  colons:\n'
                     '    max-spaces-before: 1337\n')
            f1.flush()
            f2.write('extends: ' + f1.name + '\n'
                     'rules:\n'
                     '  colons: disable\n')
            f2.flush()
            c = config.YamlLintConfig('extends: ' + f2.name + '\n'
                                      'rules:\n'
                                      '  colons: enable\n')

        self.assertEqual(c.rules['colons']['max-spaces-before'], 0)
        self.assertEqual(c.rules['colons']['max-spaces-after'], 1)


class ExtendedLibraryConfigTestCase(unittest.TestCase):
    def test_extend_config_disable_rule(self):
        old = config.YamlLintConfig('extends: default')
        new = config.YamlLintConfig('extends: default\n'
                                    'rules:\n'
                                    '  trailing-spaces: disable\n')

        old.rules['trailing-spaces'] = False

        self.assertEqual(sorted(new.rules.keys()), sorted(old.rules.keys()))
        for rule in new.rules:
            self.assertEqual(new.rules[rule], old.rules[rule])

    def test_extend_config_override_whole_rule(self):
        old = config.YamlLintConfig('extends: default')
        new = config.YamlLintConfig('extends: default\n'
                                    'rules:\n'
                                    '  empty-lines:\n'
                                    '    max: 42\n'
                                    '    max-start: 43\n'
                                    '    max-end: 44\n')

        old.rules['empty-lines']['max'] = 42
        old.rules['empty-lines']['max-start'] = 43
        old.rules['empty-lines']['max-end'] = 44

        self.assertEqual(sorted(new.rules.keys()), sorted(old.rules.keys()))
        for rule in new.rules:
            self.assertEqual(new.rules[rule], old.rules[rule])
        self.assertEqual(new.rules['empty-lines']['max'], 42)
        self.assertEqual(new.rules['empty-lines']['max-start'], 43)
        self.assertEqual(new.rules['empty-lines']['max-end'], 44)

    def test_extend_config_override_rule_partly(self):
        old = config.YamlLintConfig('extends: default')
        new = config.YamlLintConfig('extends: default\n'
                                    'rules:\n'
                                    '  empty-lines:\n'
                                    '    max-start: 42\n')

        old.rules['empty-lines']['max-start'] = 42

        self.assertEqual(sorted(new.rules.keys()), sorted(old.rules.keys()))
        for rule in new.rules:
            self.assertEqual(new.rules[rule], old.rules[rule])
        self.assertEqual(new.rules['empty-lines']['max'], 2)
        self.assertEqual(new.rules['empty-lines']['max-start'], 42)
        self.assertEqual(new.rules['empty-lines']['max-end'], 0)


class IgnorePathConfigTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(IgnorePathConfigTestCase, cls).setUpClass()

        bad_yaml = ('---\n'
                    '- key: val1\n'
                    '  key: val2\n'
                    '- trailing space \n'
                    '-    lonely hyphen\n')

        cls.wd = build_temp_workspace({
            'bin/file.lint-me-anyway.yaml': bad_yaml,
            'bin/file.yaml': bad_yaml,
            'file-at-root.yaml': bad_yaml,
            'file.dont-lint-me.yaml': bad_yaml,
            'ign-dup/file.yaml': bad_yaml,
            'ign-dup/sub/dir/file.yaml': bad_yaml,
            'ign-trail/file.yaml': bad_yaml,
            'include/ign-dup/sub/dir/file.yaml': bad_yaml,
            's/s/ign-trail/file.yaml': bad_yaml,
            's/s/ign-trail/s/s/file.yaml': bad_yaml,
            's/s/ign-trail/s/s/file2.lint-me-anyway.yaml': bad_yaml,

            '.yamllint': 'ignore: |\n'
                         '  *.dont-lint-me.yaml\n'
                         '  /bin/\n'
                         '  !/bin/*.lint-me-anyway.yaml\n'
                         '\n'
                         'extends: default\n'
                         '\n'
                         'rules:\n'
                         '  key-duplicates:\n'
                         '    ignore: |\n'
                         '      /ign-dup\n'
                         '  trailing-spaces:\n'
                         '    ignore: |\n'
                         '      ign-trail\n'
                         '      !*.lint-me-anyway.yaml\n',
        })

        cls.backup_wd = os.getcwd()
        os.chdir(cls.wd)

    @classmethod
    def tearDownClass(cls):
        super(IgnorePathConfigTestCase, cls).tearDownClass()

        os.chdir(cls.backup_wd)

        shutil.rmtree(cls.wd)

    def test_run_with_ignored_path(self):
        sys.stdout = StringIO()
        with self.assertRaises(SystemExit):
            cli.run(('-f', 'parsable', '.'))

        out = sys.stdout.getvalue()
        out = '\n'.join(sorted(out.splitlines()))

        docstart = '[warning] missing document start "---" (document-start)'
        keydup = '[error] duplication of key "key" in mapping (key-duplicates)'
        trailing = '[error] trailing spaces (trailing-spaces)'
        hyphen = '[error] too many spaces after hyphen (hyphens)'

        self.assertEqual(out, '\n'.join((
            './.yamllint:1:1: ' + docstart,
            './bin/file.lint-me-anyway.yaml:3:3: ' + keydup,
            './bin/file.lint-me-anyway.yaml:4:17: ' + trailing,
            './bin/file.lint-me-anyway.yaml:5:5: ' + hyphen,
            './file-at-root.yaml:3:3: ' + keydup,
            './file-at-root.yaml:4:17: ' + trailing,
            './file-at-root.yaml:5:5: ' + hyphen,
            './ign-dup/file.yaml:4:17: ' + trailing,
            './ign-dup/file.yaml:5:5: ' + hyphen,
            './ign-dup/sub/dir/file.yaml:4:17: ' + trailing,
            './ign-dup/sub/dir/file.yaml:5:5: ' + hyphen,
            './ign-trail/file.yaml:3:3: ' + keydup,
            './ign-trail/file.yaml:5:5: ' + hyphen,
            './include/ign-dup/sub/dir/file.yaml:3:3: ' + keydup,
            './include/ign-dup/sub/dir/file.yaml:4:17: ' + trailing,
            './include/ign-dup/sub/dir/file.yaml:5:5: ' + hyphen,
            './s/s/ign-trail/file.yaml:3:3: ' + keydup,
            './s/s/ign-trail/file.yaml:5:5: ' + hyphen,
            './s/s/ign-trail/s/s/file.yaml:3:3: ' + keydup,
            './s/s/ign-trail/s/s/file.yaml:5:5: ' + hyphen,
            './s/s/ign-trail/s/s/file2.lint-me-anyway.yaml:3:3: ' + keydup,
            './s/s/ign-trail/s/s/file2.lint-me-anyway.yaml:4:17: ' + trailing,
            './s/s/ign-trail/s/s/file2.lint-me-anyway.yaml:5:5: ' + hyphen,
        )))
