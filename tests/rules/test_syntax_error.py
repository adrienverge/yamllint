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

from tests.rules.common import RuleTestCase


class YamlLintTestCase(RuleTestCase):
    rule_id = None  # syntax error

    def test_lint(self):
        self.check('---\n'
                   'this is not: valid: YAML\n', None, problem=(2, 19))
        self.check('---\n'
                   'this is: valid YAML\n'
                   '\n'
                   'this is an error: [\n'
                   '\n'
                   '...\n', None, problem=(6, 1))

    def test_directives(self):
        self.check('%YAML 1.2\n'
                   '%TAG ! tag:clarkevans.com,2002:\n'
                   'doc: ument\n'
                   '...\n', None, problem=(3, 1))
