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
import shutil
import tempfile

from tests.common import RuleTestCase
from yamllint.config import YamlLintConfigError


class CustomTestCase(RuleTestCase):
    rule_id = 'custom'

    @classmethod
    def setUpClass(self):
        self.tmpd = tempfile.mkdtemp()
        rules = os.path.join(self.tmpd, '.yamllint', 'rules')
        os.makedirs(rules)

        with open(os.path.join(rules, '__init__.py'), 'w'):
            pass

        with open(os.path.join(rules, 'custom.py'), 'w') as f:
            f.write("""ID = 'custom'
TYPE = 'token'

def check(*args, **kwargs):
    if 0:
        yield
""")

        self.orig_cwd = os.getcwd()
        os.chdir(self.tmpd)

    def test_disabled(self):
        conf = 'custom: disable\n'

        self.check('---\n', conf)

    def test_enabled(self):
        conf = 'custom: enable\n'

        self.check('---\n', conf)

    def test_config_present(self):
        conf = 'custom: enable\n'

        self.check('---\n', conf)

    def test_config_missing(self):
        conf = ''

        with self.assertRaises(YamlLintConfigError):
            self.check('---\n', conf)

    @classmethod
    def tearDownClass(self):
        os.chdir(self.orig_cwd)
        shutil.rmtree(self.tmpd)
