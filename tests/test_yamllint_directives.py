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

from tests.common import RuleTestCase


class YamllintDirectivesTestCase(RuleTestCase):
    conf = ('commas: disable\n'
            'trailing-spaces: {}\n'
            'colons: {max-spaces-before: 1}\n')

    def test_disable_directive(self):
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 18, 'trailing-spaces'),
                   problem2=(4, 8, 'colons'),
                   problem3=(6, 7, 'colons'),
                   problem4=(6, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '# yamllint disable\n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem=(3, 18, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '# yamllint disable\n'
                   '- trailing spaces    \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '# yamllint enable\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(8, 7, 'colons'),
                   problem2=(8, 26, 'trailing-spaces'))

    def test_disable_directive_with_rules(self):
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '# yamllint disable rule:trailing-spaces\n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 18, 'trailing-spaces'),
                   problem2=(5, 8, 'colons'),
                   problem3=(7, 7, 'colons'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '# yamllint disable rule:trailing-spaces\n'
                   '- trailing spaces    \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '# yamllint enable rule:trailing-spaces\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(5, 8, 'colons'),
                   problem2=(8, 7, 'colons'),
                   problem3=(8, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '# yamllint disable rule:trailing-spaces\n'
                   '- trailing spaces    \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '# yamllint enable\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(5, 8, 'colons'),
                   problem2=(8, 7, 'colons'),
                   problem3=(8, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '# yamllint disable\n'
                   '- trailing spaces    \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '# yamllint enable rule:trailing-spaces\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem=(8, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '# yamllint disable rule:colons\n'
                   '- trailing spaces    \n'
                   '# yamllint disable rule:trailing-spaces\n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '# yamllint enable rule:colons\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(4, 18, 'trailing-spaces'),
                   problem2=(9, 7, 'colons'))

    def test_disable_line_directive(self):
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '# yamllint disable-line\n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 18, 'trailing-spaces'),
                   problem2=(7, 7, 'colons'),
                   problem3=(7, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '- bad   : colon  # yamllint disable-line\n'
                   '- [valid , YAML]\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 18, 'trailing-spaces'),
                   problem2=(6, 7, 'colons'),
                   problem3=(6, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]  # yamllint disable-line\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 18, 'trailing-spaces'),
                   problem2=(4, 8, 'colons'),
                   problem3=(6, 7, 'colons'),
                   problem4=(6, 26, 'trailing-spaces'))

    def test_disable_line_directive_with_rules(self):
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '# yamllint disable-line rule:colons\n'
                   '- trailing spaces    \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(4, 18, 'trailing-spaces'),
                   problem2=(5, 8, 'colons'),
                   problem3=(7, 7, 'colons'),
                   problem4=(7, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces  # yamllint disable-line rule:colons  \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 55, 'trailing-spaces'),
                   problem2=(4, 8, 'colons'),
                   problem3=(6, 7, 'colons'),
                   problem4=(6, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '# yamllint disable-line rule:colons\n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 18, 'trailing-spaces'),
                   problem2=(7, 7, 'colons'),
                   problem3=(7, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '- bad   : colon  # yamllint disable-line rule:colons\n'
                   '- [valid , YAML]\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 18, 'trailing-spaces'),
                   problem2=(6, 7, 'colons'),
                   problem3=(6, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '# yamllint disable-line rule:colons\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 18, 'trailing-spaces'),
                   problem2=(4, 8, 'colons'),
                   problem3=(7, 26, 'trailing-spaces'))
        self.check('---\n'
                   '- [valid , YAML]\n'
                   '- trailing spaces    \n'
                   '- bad   : colon\n'
                   '- [valid , YAML]\n'
                   '# yamllint disable-line rule:colons rule:trailing-spaces\n'
                   '- bad  : colon and spaces   \n'
                   '- [valid , YAML]\n',
                   self.conf,
                   problem1=(3, 18, 'trailing-spaces'),
                   problem2=(4, 8, 'colons'))

    def test_directive_on_last_line(self):
        conf = 'new-line-at-end-of-file: {}'
        self.check('---\n'
                   'no new line',
                   conf,
                   problem=(2, 12, 'new-line-at-end-of-file'))
        self.check('---\n'
                   '# yamllint disable\n'
                   'no new line',
                   conf)
        self.check('---\n'
                   'no new line  # yamllint disable',
                   conf)

    def test_indented_directive(self):
        conf = 'brackets: {min-spaces-inside: 0, max-spaces-inside: 0}'
        self.check('---\n'
                   '- a: 1\n'
                   '  b:\n'
                   '    c: [    x]\n',
                   conf,
                   problem=(4, 12, 'brackets'))
        self.check('---\n'
                   '- a: 1\n'
                   '  b:\n'
                   '    # yamllint disable-line rule:brackets\n'
                   '    c: [    x]\n',
                   conf)

    def test_directive_on_itself(self):
        conf = ('comments: {min-spaces-from-content: 2}\n'
                'comments-indentation: {}\n')
        self.check('---\n'
                   '- a: 1 # comment too close\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf,
                   problem1=(2, 8, 'comments'),
                   problem2=(4, 2, 'comments-indentation'))
        self.check('---\n'
                   '# yamllint disable\n'
                   '- a: 1 # comment too close\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf)
        self.check('---\n'
                   '- a: 1 # yamllint disable-line\n'
                   '  b:\n'
                   '    # yamllint disable-line\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf)
        self.check('---\n'
                   '- a: 1 # yamllint disable-line rule:comments\n'
                   '  b:\n'
                   '    # yamllint disable-line rule:comments-indentation\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf)
        self.check('---\n'
                   '# yamllint disable\n'
                   '- a: 1 # comment too close\n'
                   '  # yamllint enable rule:comments-indentation\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf,
                   problem=(6, 2, 'comments-indentation'))

    def test_disable_file_directive(self):
        conf = ('comments: {min-spaces-from-content: 2}\n'
                'comments-indentation: {}\n')
        self.check('# yamllint disable-file\n'
                   '---\n'
                   '- a: 1 # comment too close\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf)
        self.check('#    yamllint disable-file\n'
                   '---\n'
                   '- a: 1 # comment too close\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf)
        self.check('#yamllint disable-file\n'
                   '---\n'
                   '- a: 1 # comment too close\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf)
        self.check('#yamllint disable-file    \n'
                   '---\n'
                   '- a: 1 # comment too close\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf)
        self.check('---\n'
                   '# yamllint disable-file\n'
                   '- a: 1 # comment too close\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf,
                   problem1=(3, 8, 'comments'),
                   problem2=(5, 2, 'comments-indentation'))
        self.check('# yamllint disable-file: rules cannot be specified\n'
                   '---\n'
                   '- a: 1 # comment too close\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf,
                   problem1=(3, 8, 'comments'),
                   problem2=(5, 2, 'comments-indentation'))
        self.check('AAAA yamllint disable-file\n'
                   '---\n'
                   '- a: 1 # comment too close\n'
                   '  b:\n'
                   ' # wrong indentation\n'
                   '    c: [x]\n',
                   conf,
                   problem1=(1, 1, 'document-start'),
                   problem2=(3, 8, 'comments'),
                   problem3=(5, 2, 'comments-indentation'))

    def test_disable_file_directive_not_at_first_position(self):
        self.check('# yamllint disable-file\n'
                   '---\n'
                   '- bad  : colon and spaces   \n',
                   self.conf)
        self.check('---\n'
                   '# yamllint disable-file\n'
                   '- bad  : colon and spaces   \n',
                   self.conf,
                   problem1=(3, 7, 'colons'),
                   problem2=(3, 26, 'trailing-spaces'))

    def test_disable_file_directive_with_syntax_error(self):
        self.check('# This file is not valid YAML (it is a Jinja template)\n'
                   '{% if extra_info %}\n'
                   'key1: value1\n'
                   '{% endif %}\n'
                   'key2: value2\n',
                   self.conf,
                   problem=(2, 2, 'syntax'))
        self.check('# yamllint disable-file\n'
                   '# This file is not valid YAML (it is a Jinja template)\n'
                   '{% if extra_info %}\n'
                   'key1: value1\n'
                   '{% endif %}\n'
                   'key2: value2\n',
                   self.conf)

    def test_disable_file_directive_with_dos_lines(self):
        self.check('# yamllint disable-file\r\n'
                   '---\r\n'
                   '- bad  : colon and spaces   \r\n',
                   self.conf)
        self.check('# yamllint disable-file\r\n'
                   '# This file is not valid YAML (it is a Jinja template)\r\n'
                   '{% if extra_info %}\r\n'
                   'key1: value1\r\n'
                   '{% endif %}\r\n'
                   'key2: value2\r\n',
                   self.conf)
