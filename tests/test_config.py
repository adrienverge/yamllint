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

import os
import unittest

from yamllint import config


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.base = config.parse_config_from_file(os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            'yamllint', 'conf', 'default.yml'))

    def test_extend_config_disable_rule(self):
        new = config.parse_config('extends: default\n'
                                  'rules:\n'
                                  '  trailing-spaces: disable\n')

        base = self.base.copy()
        del base['trailing-spaces']

        self.assertEqual(sorted(new.keys()), sorted(base.keys()))
        for rule in new:
            self.assertEqual(new[rule], base[rule])

    def test_extend_config_override_whole_rule(self):
        new = config.parse_config('extends: default\n'
                                  'rules:\n'
                                  '  empty-lines:\n'
                                  '    max: 42\n'
                                  '    max-start: 43\n'
                                  '    max-end: 44\n')

        base = self.base.copy()
        base['empty-lines']['max'] = 42
        base['empty-lines']['max-start'] = 43
        base['empty-lines']['max-end'] = 44

        self.assertEqual(sorted(new.keys()), sorted(base.keys()))
        for rule in new:
            self.assertEqual(new[rule], base[rule])

    def test_extend_config_override_rule_partly(self):
        new = config.parse_config('extends: default\n'
                                  'rules:\n'
                                  '  empty-lines:\n'
                                  '    max-start: 42\n')

        base = self.base.copy()
        base['empty-lines']['max-start'] = 42

        self.assertEqual(sorted(new.keys()), sorted(base.keys()))
        for rule in new:
            self.assertEqual(new[rule], base[rule])
