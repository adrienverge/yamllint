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

import unittest

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

        self.assertEqual(len(new.enabled_rules()), 1)

    def test_unknown_rule(self):
        with self.assertRaisesRegexp(
                config.YamlLintConfigError,
                'invalid config: no such rule: "this-one-does-not-exist"'):
            config.YamlLintConfig('rules:\n'
                                  '  this-one-does-not-exist: {}\n')

    def test_missing_option(self):
        with self.assertRaisesRegexp(
                config.YamlLintConfigError,
                'invalid config: missing option "max-spaces-before" '
                'for rule "colons"'):
            config.YamlLintConfig('rules:\n'
                                  '  colons:\n'
                                  '    max-spaces-after: 1\n')

    def test_unknown_option(self):
        with self.assertRaisesRegexp(
                config.YamlLintConfigError,
                'invalid config: unknown option "abcdef" for rule "colons"'):
            config.YamlLintConfig('rules:\n'
                                  '  colons:\n'
                                  '    max-spaces-before: 0\n'
                                  '    max-spaces-after: 1\n'
                                  '    abcdef: yes\n')


class ExtendedConfigTestCase(unittest.TestCase):
    def test_extend_add_rule(self):
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

        self.assertEqual(len(new.enabled_rules()), 2)

    def test_extend_remove_rule(self):
        old = config.YamlLintConfig('rules:\n'
                                    '  colons:\n'
                                    '    max-spaces-before: 0\n'
                                    '    max-spaces-after: 1\n'
                                    '  hyphens:\n'
                                    '    max-spaces-after: 2\n')
        new = config.YamlLintConfig('rules:\n'
                                    '  colons: disable\n')
        new.extend(old)

        self.assertEqual(sorted(new.rules.keys()), ['colons', 'hyphens'])
        self.assertEqual(new.rules['colons'], False)
        self.assertEqual(new.rules['hyphens']['max-spaces-after'], 2)

        self.assertEqual(len(new.enabled_rules()), 1)

    def test_extend_edit_rule(self):
        old = config.YamlLintConfig('rules:\n'
                                    '  colons:\n'
                                    '    max-spaces-before: 0\n'
                                    '    max-spaces-after: 1\n'
                                    '  hyphens:\n'
                                    '    max-spaces-after: 2\n')
        new = config.YamlLintConfig('rules:\n'
                                    '  colons:\n'
                                    '    max-spaces-before: 3\n'
                                    '    max-spaces-after: 4\n')
        new.extend(old)

        self.assertEqual(sorted(new.rules.keys()), ['colons', 'hyphens'])
        self.assertEqual(new.rules['colons']['max-spaces-before'], 3)
        self.assertEqual(new.rules['colons']['max-spaces-after'], 4)
        self.assertEqual(new.rules['hyphens']['max-spaces-after'], 2)

        self.assertEqual(len(new.enabled_rules()), 2)

    def test_extend_reenable_rule(self):
        old = config.YamlLintConfig('rules:\n'
                                    '  colons:\n'
                                    '    max-spaces-before: 0\n'
                                    '    max-spaces-after: 1\n'
                                    '  hyphens: disable\n')
        new = config.YamlLintConfig('rules:\n'
                                    '  hyphens:\n'
                                    '    max-spaces-after: 2\n')
        new.extend(old)

        self.assertEqual(sorted(new.rules.keys()), ['colons', 'hyphens'])
        self.assertEqual(new.rules['colons']['max-spaces-before'], 0)
        self.assertEqual(new.rules['colons']['max-spaces-after'], 1)
        self.assertEqual(new.rules['hyphens']['max-spaces-after'], 2)

        self.assertEqual(len(new.enabled_rules()), 2)


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
