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


HIT_ANCHOR_POINTER = '''---
key: &keyanchor a
otherkey: *keyanchor
'''
MISS_ANCHOR_POINTER = '''---
key: &keyanchor a
otherkey: *missedkeyanchor
'''

HIT_ANCHOR_MERGE = '''---
block: &keyanchor
  key: a
otherkey:
  <<: *keyanchor
  otherkey: b
'''
MISS_ANCHOR_MERGE = '''---
block: &keyanchor
  key: a
otherkey:
  <<: *missedkeyanchor
  otherkey: b
'''

MULTI_HIT_ANCHOR_POINTER = '''---
key: &keyanchor a
otherkey: *keyanchor
otherotherkey: *keyanchor
'''
MULTI_MISS_ANCHOR_POINTER = '''---
key: &keyanchor a
otherkey: *missedkeyanchor
otherotherkey: *missedkeyanchor
'''

MULTI_DOC_HIT_ANCHOR_POINTER = '''---
key: &keyanchor a
otherkey: *keyanchor
---
key: &otherkeyanchor a
otherkey: *otherkeyanchor
'''
MULTI_DOC_MISS_ANCHOR_POINTER = '''---
key: &keyanchor a
otherkey: *missedkeyanchor
---
key: &otherkeyanchor a
otherkey: *othermissedkeyanchor
'''


class UnknownAliasesTestCase(RuleTestCase):
    rule_id = 'unknown-aliases'

    def test_disabled(self):
        conf = 'unknown-aliases: disable'

        self.check(HIT_ANCHOR_POINTER, conf)
        self.check(HIT_ANCHOR_MERGE, conf)
        self.check(MULTI_HIT_ANCHOR_POINTER, conf)
        self.check(MULTI_DOC_HIT_ANCHOR_POINTER, conf)

        self.check(MISS_ANCHOR_POINTER, conf)
        self.check(MISS_ANCHOR_MERGE, conf)
        self.check(MULTI_MISS_ANCHOR_POINTER, conf)
        self.check(MULTI_DOC_MISS_ANCHOR_POINTER, conf)

    def test_enabled(self):
        conf = 'unknown-aliases: enable'

        self.check(HIT_ANCHOR_POINTER, conf)
        self.check(HIT_ANCHOR_MERGE, conf)
        self.check(MULTI_HIT_ANCHOR_POINTER, conf)
        self.check(MULTI_DOC_HIT_ANCHOR_POINTER, conf)

        self.check(MISS_ANCHOR_POINTER, conf, problem=(3,11))
        self.check(MISS_ANCHOR_MERGE, conf, problem=(5, 7))
        self.check(MULTI_MISS_ANCHOR_POINTER, conf,
                   problem1=(3, 11), problem2=(4, 16))
        self.check(MULTI_DOC_MISS_ANCHOR_POINTER, conf,
                   problem1=(3, 11), problem2=(6, 11))
