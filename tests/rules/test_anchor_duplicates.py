# Copyright (C) 2021 Sergei Mikhailov
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


NORMAL_ANCHOR = '''---
key: &keyanchor a
otherkey: *keyanchor
'''

DUPLICATED_ANCHOR = '''---
key1: &keyanchor a
key2: &keyanchor b
otherkey: *keyanchor
'''


class AnchorDuplicatesTestCase(RuleTestCase):
    rule_id = 'anchor-duplicates'

    def test_disabled(self):
        conf = 'anchor-duplicates: disable'

        self.check(NORMAL_ANCHOR, conf)
        self.check(DUPLICATED_ANCHOR, conf)

    def test_enabled(self):
        conf = 'anchor-duplicates: enable'

        self.check(NORMAL_ANCHOR, conf)
        self.check(DUPLICATED_ANCHOR, conf, problem=(3,7))
