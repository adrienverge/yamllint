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

from io import open
import os

from tests.common import RuleTestCase


# This file checks examples from YAML 1.2 specification [1] against yamllint.
#
# [1]: http://www.yaml.org/spec/1.2/spec.html
#
# Example files generated with:
#
#     from bs4 import BeautifulSoup
#     with open('spec.html', encoding='iso-8859-1') as f:
#         soup = BeautifulSoup(f, 'lxml')
#         for ex in soup.find_all('div', class_='example'):
#             title = ex.find('p', class_='title').find('b').get_text()
#             id = '-'.join(title.split('\xa0')[:2])[:-1].lower()
#             span = ex.find('span', class_='database')
#             for br in span.find_all("br"):
#                 br.replace_with("\n")
#             text = text.replace('\u2193', '')    # downwards arrow
#             text = text.replace('\u21d3', '')    # double downwards arrow
#             text = text.replace('\u00b7', ' ')   # visible space
#             text = text.replace('\u21d4', '')    # byte order mark
#             text = text.replace('\u2192', '\t')  # right arrow
#             text = text.replace('\u00b0', '')    # empty scalar
#             with open('tests/yaml-1.2-spec-examples/%s' % id, 'w',
#                       encoding='utf-8') as g:
#                 g.write(text)

class SpecificationTestCase(RuleTestCase):
    rule_id = None


conf_general = ('document-start: disable\n'
                'comments: {min-spaces-from-content: 1}\n'
                'braces: {min-spaces-inside: 1, max-spaces-inside: 1}\n'
                'brackets: {min-spaces-inside: 1, max-spaces-inside: 1}\n')
conf_overrides = {
    'example-2.2': 'colons: {max-spaces-after: 2}\n',
    'example-2.4': 'colons: {max-spaces-after: 3}\n',
    'example-2.5': ('empty-lines: {max-end: 2}\n'
                    'brackets: {min-spaces-inside: 0, max-spaces-inside: 2}\n'
                    'commas: {max-spaces-before: -1}\n'),
    'example-2.6': ('braces: {min-spaces-inside: 0, max-spaces-inside: 0}\n'
                    'indentation: disable\n'),
    'example-2.12': ('empty-lines: {max-end: 1}\n'
                     'colons: {max-spaces-before: -1}\n'),
    'example-2.16': 'empty-lines: {max-end: 1}\n',
    'example-2.18': 'empty-lines: {max-end: 1}\n',
    'example-2.19': 'empty-lines: {max-end: 1}\n',
    'example-2.28': 'empty-lines: {max-end: 3}\n',
    'example-5.3': ('indentation: {indent-sequences: false}\n'
                    'colons: {max-spaces-before: 1}\n'),
    'example-6.4': 'trailing-spaces: disable\n',
    'example-6.5': 'trailing-spaces: disable\n',
    'example-6.6': 'trailing-spaces: disable\n',
    'example-6.7': 'trailing-spaces: disable\n',
    'example-6.8': 'trailing-spaces: disable\n',
    'example-6.10': ('empty-lines: {max-end: 2}\n'
                     'trailing-spaces: disable\n'
                     'comments-indentation: disable\n'),
    'example-6.11': ('empty-lines: {max-end: 1}\n'
                     'comments-indentation: disable\n'),
    'example-6.13': 'comments-indentation: disable\n',
    'example-6.14': 'comments-indentation: disable\n',
    'example-6.23': 'colons: {max-spaces-before: 1}\n',
    'example-7.4': ('colons: {max-spaces-before: 1}\n'
                    'indentation: disable\n'),
    'example-7.5': 'trailing-spaces: disable\n',
    'example-7.6': 'trailing-spaces: disable\n',
    'example-7.7': 'indentation: disable\n',
    'example-7.8': ('colons: {max-spaces-before: 1}\n'
                    'indentation: disable\n'),
    'example-7.9': 'trailing-spaces: disable\n',
    'example-7.11': ('colons: {max-spaces-before: 1}\n'
                     'indentation: disable\n'),
    'example-7.13': ('brackets: {min-spaces-inside: 0, max-spaces-inside: 1}\n'
                     'commas: {max-spaces-before: 1, min-spaces-after: 0}\n'),
    'example-7.14': 'indentation: disable\n',
    'example-7.15': ('braces: {min-spaces-inside: 0, max-spaces-inside: 1}\n'
                     'commas: {max-spaces-before: 1, min-spaces-after: 0}\n'
                     'colons: {max-spaces-before: 1}\n'),
    'example-7.16': 'indentation: disable\n',
    'example-7.17': 'indentation: disable\n',
    'example-7.18': 'indentation: disable\n',
    'example-7.19': 'indentation: disable\n',
    'example-7.20': ('colons: {max-spaces-before: 1}\n'
                     'indentation: disable\n'),
    'example-8.1': 'empty-lines: {max-end: 1}\n',
    'example-8.2': 'trailing-spaces: disable\n',
    'example-8.5': ('comments-indentation: disable\n'
                    'trailing-spaces: disable\n'),
    'example-8.6': 'empty-lines: {max-end: 1}\n',
    'example-8.7': 'empty-lines: {max-end: 1}\n',
    'example-8.8': 'trailing-spaces: disable\n',
    'example-8.9': 'empty-lines: {max-end: 1}\n',
    'example-8.14': 'colons: {max-spaces-before: 1}\n',
    'example-8.16': 'indentation: {spaces: 1}\n',
    'example-8.17': 'indentation: disable\n',
    'example-8.20': ('indentation: {indent-sequences: false}\n'
                     'colons: {max-spaces-before: 1}\n'),
    'example-8.22': 'indentation: disable\n',
    'example-10.1': 'colons: {max-spaces-before: 2}\n',
    'example-10.2': 'indentation: {indent-sequences: false}\n',
    'example-10.8': 'truthy: disable\n',
    'example-10.9': 'truthy: disable\n',
}

files = os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'yaml-1.2-spec-examples'))
assert len(files) == 132


def _gen_test(buffer, conf):
    def test(self):
        self.check(buffer, conf)
    return test


# The following tests are blacklisted (i.e. will not be checked against
# yamllint), because pyyaml is currently not able to parse the contents
# (using yaml.parse()).
pyyaml_blacklist = (
    'example-2.11',
    'example-2.23',
    'example-2.24',
    'example-2.27',
    'example-5.10',
    'example-5.12',
    'example-5.13',
    'example-5.14',
    'example-5.6',
    'example-6.1',
    'example-6.12',
    'example-6.15',
    'example-6.17',
    'example-6.18',
    'example-6.19',
    'example-6.2',
    'example-6.20',
    'example-6.21',
    'example-6.22',
    'example-6.24',
    'example-6.25',
    'example-6.26',
    'example-6.27',
    'example-6.3',
    'example-7.1',
    'example-7.10',
    'example-7.12',
    'example-7.17',
    'example-7.2',
    'example-7.21',
    'example-7.22',
    'example-7.3',
    'example-8.18',
    'example-8.19',
    'example-8.21',
    'example-8.3',
    'example-9.3',
    'example-9.4',
    'example-9.5',
)

for file in files:
    if file in pyyaml_blacklist:
        continue

    with open('tests/yaml-1.2-spec-examples/' + file, encoding='utf-8') as f:
        conf = conf_general + conf_overrides.get(file, '')
        setattr(SpecificationTestCase, 'test_' + file,
                _gen_test(f.read(), conf))
