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
import warnings

try:
    from unittest import mock
except ImportError:  # for python 2.7
    mock = False

from tests.plugins import example

import yamllint.plugins


class FakeEntryPoint(object):
    """Fake object to mimic pkg_resources.EntryPoint.
    """
    RULES_MAP = example.RULES_MAP

    def load(self):
        """Fake method to return self.
        """
        return self


class BrokenEntryPoint(FakeEntryPoint):
    """Fake object to mimic load failure of pkg_resources.EntryPoint.
    """
    def load(self):
        raise ImportError("This entry point should fail always!")


class PluginFunctionsTestCase(unittest.TestCase):

    def test_validate_rule_module(self):
        fun = yamllint.plugins.validate_rule_module
        rule_mod = example.override_comments

        self.assertFalse(fun(object()))
        self.assertTrue(fun(rule_mod))

    @unittest.skipIf(not mock, "unittest.mock is not available")
    def test_validate_rule_module_using_mock(self):
        fun = yamllint.plugins.validate_rule_module
        rule_mod = example.override_comments

        with mock.patch.object(rule_mod, "ID", False):
            self.assertFalse(fun(rule_mod))

        with mock.patch.object(rule_mod, "TYPE", False):
            self.assertFalse(fun(rule_mod))

        with mock.patch.object(rule_mod, "check", True):
            self.assertFalse(fun(rule_mod))

    def test_load_plugin_rules_itr(self):
        fun = yamllint.plugins.load_plugin_rules_itr

        self.assertEqual(list(fun([])), [])
        self.assertEqual(sorted(fun([FakeEntryPoint(),
                                     FakeEntryPoint()])),
                         sorted(FakeEntryPoint.RULES_MAP.items()))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.assertEqual(list(fun([BrokenEntryPoint()])), [])
