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

from tests.common import RuleTestCase


class YamlLintTestCase(RuleTestCase):
    rule_id = None  # syntax error

    def test_syntax_errors(self):
        self.check('---\n'
                   'this is not: valid: YAML\n', None, problem=(2, 19))
        self.check('---\n'
                   'this is: valid YAML\n'
                   '\n'
                   'this is an error: [\n'
                   '\n'
                   '...\n', None, problem=(6, 1))
        self.check('%YAML 1.2\n'
                   '%TAG ! tag:clarkevans.com,2002:\n'
                   'doc: ument\n'
                   '...\n', None, problem=(3, 1))

    def test_non_printable_characters(self):
        # PyYAML rejects non-printable characters (control characters such as
        # NUL or DEL) with a ReaderError, which is a YAMLError but not a
        # MarkedYAMLError. yamllint must report these as syntax errors instead
        # of letting the exception escape.
        self.check('---\n'
                   'key: val\x00ue\n', None, problem=(2, 9))
        self.check('---\n'
                   'this is ok\n'
                   'this has a \x01 control char\n', None, problem=(3, 12))
        self.check('\x7f\n', None, problem=(1, 1))
        # A bare non-printable character with no other content.
        self.check('\x00', None, problem=(1, 1))
        # Cosmetic rules still run on the printable lines preceding the error.
        self.check('---\n'
                   'trailing:   \n'
                   'oops\x00\n', None,
                   problem1=(2, 10, 'trailing-spaces'),
                   problem2=(3, 5))

    def test_empty_flows(self):
        self.check('---\n'
                   '- []\n'
                   '- {}\n'
                   '- [\n'
                   ']\n'
                   '- {\n'
                   '}\n'
                   '...\n', None)

    def test_explicit_mapping(self):
        self.check('---\n'
                   '? key\n'
                   ': - value 1\n'
                   '  - value 2\n'
                   '...\n', None)
        self.check('---\n'
                   '?\n'
                   '  key\n'
                   ': {a: 1}\n'
                   '...\n', None)
        self.check('---\n'
                   '?\n'
                   '  key\n'
                   ':\n'
                   '  val\n'
                   '...\n', None)

    def test_mapping_between_sequences(self):
        # This is valid YAML. See http://www.yaml.org/spec/1.2/spec.html,
        # example 2.11
        self.check('---\n'
                   '? - Detroit Tigers\n'
                   '  - Chicago cubs\n'
                   ':\n'
                   '  - 2001-07-23\n'
                   '\n'
                   '? [New York Yankees,\n'
                   '   Atlanta Braves]\n'
                   ': [2001-07-02, 2001-08-12,\n'
                   '   2001-08-14]\n', None)

    def test_sets(self):
        self.check('---\n'
                   '? key one\n'
                   '? key two\n'
                   '? [non, scalar, key]\n'
                   '? key with value\n'
                   ': value\n'
                   '...\n', None)
        self.check('---\n'
                   '? - multi\n'
                   '  - line\n'
                   '  - keys\n'
                   '? in:\n'
                   '    a:\n'
                   '      set\n'
                   '...\n', None)
