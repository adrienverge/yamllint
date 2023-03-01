# Copyright (C) 2023 Johannes F. Knauf and Kevin Wojniak
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

import locale

from tests.common import RuleTestCase


class ListOrderingTestCase(RuleTestCase):
    rule_id = 'list-ordering'

    def test_disabled(self):
        conf = 'list-ordering: disable'
        self.check('---\n'
                   '- seconditem\n'
                   '- firstitem\n', conf)
        self.check('---\n'
                   '[seconditem, firstitem]\n', conf)
        self.check('---\n'
                   '- second\n'
                   '- at\n', conf)

    def test_enabled(self):
        conf = 'list-ordering: enable'
        self.check('---\n'
                   '- seconditem\n'
                   '- firstitem\n', conf,
                   problem=(3, 3))
        self.check('---\n'
                   '[seconditem, firstitem]\n', conf,
                   problem=(2, 14))
        self.check('---\n'
                   '- second\n'
                   '- at\n', conf,
                   problem=(3, 3))
        self.check('---\n'
                   'nested but OK:\n'
                   '  - third: [second]\n'
                   '  - first\n', conf)
        self.check('---\n'
                   'nested failure:\n'
                   '  - third\n'
                   '  - first:\n'
                   '    items:\n'
                   '      - z\n'
                   '      - a\n', conf,
                   problem=(7, 9))

    def test_word_length(self):
        conf = 'list-ordering: enable'
        self.check('---\n'
                   '- a\n'
                   '- ab\n'
                   '- abc\n', conf)
        self.check('---\n'
                   '- a\n'
                   '- abc\n'
                   '- ab\n', conf,
                   problem=(4, 3))

    def test_case(self):
        conf = 'list-ordering: enable'
        self.check('---\n'
                   '- T-shirt\n'
                   '- T-shirts\n'
                   '- t-shirt\n'
                   '- t-shirts\n', conf)
        self.check('---\n'
                   '- T-shirt\n'
                   '- t-shirt\n'
                   '- T-shirts\n'
                   '- t-shirts\n', conf,
                   problem=(4, 3))

    def test_accents(self):
        conf = 'list-ordering: enable'
        self.check('---\n'
                   '- hair\n'
                   '- hais\n'
                   '- haïr\n'
                   '- haïssable\n', conf)
        self.check('---\n'
                   '- haïr\n'
                   '- hais\n', conf,
                   problem=(3, 3))

    def test_locale_case(self):
        self.addCleanup(locale.setlocale, locale.LC_ALL, (None, None))
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except locale.Error:  # pragma: no cover
            self.skipTest('locale en_US.UTF-8 not available')
        conf = ('list-ordering: enable')
        self.check('---\n'
                   '- t-shirt\n'
                   '- T-shirt\n'
                   '- t-shirts\n'
                   '- T-shirts\n', conf)
        self.check('---\n'
                   '- t-shirt\n'
                   '- t-shirts\n'
                   '- T-shirt\n'
                   '- T-shirts\n', conf,
                   problem=(4, 3))

    def test_locale_accents(self):
        self.addCleanup(locale.setlocale, locale.LC_ALL, (None, None))
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except locale.Error:  # pragma: no cover
            self.skipTest('locale en_US.UTF-8 not available')
        conf = ('list-ordering: enable')
        self.check('---\n'
                   '- hair\n'
                   '- haïr\n'
                   '- hais\n'
                   '- haïssable\n', conf)
        self.check('---\n'
                   '- hais\n'
                   '- haïr\n', conf,
                   problem=(3, 3))
