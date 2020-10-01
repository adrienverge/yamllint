# -*- coding: utf-8 -*-
# Copyright (C) 2020 Satoru SATOH
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

try:
    from unittest import mock
except ImportError:  # for python 2.7
    mock = False

from tests.plugins import example

import yamllint.rules


RULE_NEVER_EXISTS = "rule_never_exists"
PLUGIN_RULES = example.RULES_MAP


class TestCase(unittest.TestCase):
    """Test cases for yamllint.rules.__init__.*.
    """
    def test_get_default_rule(self):
        self.assertEqual(yamllint.rules.get(yamllint.rules.braces.ID),
                         yamllint.rules.braces)

    def test_get_rule_does_not_exist(self):
        with self.assertRaises(ValueError):
            yamllint.rules.get(RULE_NEVER_EXISTS)


@unittest.skipIf(not mock, "unittest.mock is not available")
class TestCaseUsingMock(unittest.TestCase):
    """Test cases for yamllint.rules.__init__.* using mock.
    """
    def test_get_default_rule_with_plugins(self):
        with mock.patch.dict(yamllint.rules._EXTERNAL_RULES, PLUGIN_RULES):
            self.assertEqual(yamllint.rules.get(yamllint.rules.braces.ID),
                             yamllint.rules.braces)

    def test_get_plugin_rules(self):
        plugin_rule_id = example.override_comments.ID
        plugin_rule_mod = example.override_comments

        with mock.patch.dict(yamllint.rules._EXTERNAL_RULES, PLUGIN_RULES):
            self.assertEqual(yamllint.rules.get(plugin_rule_id),
                             plugin_rule_mod)

    def test_get_rule_does_not_exist_with_plugins(self):
        with mock.patch.dict(yamllint.rules._EXTERNAL_RULES, PLUGIN_RULES):
            with self.assertRaises(ValueError):
                yamllint.rules.get(RULE_NEVER_EXISTS)
