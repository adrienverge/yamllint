# -*- coding: utf-8 -*-
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

DUPLICATE_ANCHORS = '''---
first_block: &keyanchor
  key: a

second_block: &keyanchor
  key: b

target_block: *keyanchor
'''


class AnchorsTestCase(RuleTestCase):
    rule_id = 'anchors'

    def test_disabled(self):
        conf = 'anchors: disable'

        self.check(HIT_ANCHOR_POINTER, conf)
        self.check(HIT_ANCHOR_MERGE, conf)
        self.check(MULTI_HIT_ANCHOR_POINTER, conf)
        self.check(MULTI_DOC_HIT_ANCHOR_POINTER, conf)

        self.check(MISS_ANCHOR_POINTER, conf)
        self.check(MISS_ANCHOR_MERGE, conf)
        self.check(MULTI_MISS_ANCHOR_POINTER, conf)
        self.check(MULTI_DOC_MISS_ANCHOR_POINTER, conf)
        self.check(DUPLICATE_ANCHORS, conf)

    def test_enabled(self):
        conf = 'anchors: enable'

        self.check(HIT_ANCHOR_POINTER, conf)
        self.check(HIT_ANCHOR_MERGE, conf)
        self.check(MULTI_HIT_ANCHOR_POINTER, conf)
        self.check(MULTI_DOC_HIT_ANCHOR_POINTER, conf)

        self.check(MISS_ANCHOR_POINTER, conf,
                   problem=(3, 11))
        self.check(MISS_ANCHOR_MERGE, conf,
                   problem_first=(5, 7),
                   problem_second=(5, 7))
        self.check(MULTI_MISS_ANCHOR_POINTER, conf,
                   problem_first=(3, 11),
                   problem_second=(4, 16))
        self.check(MULTI_DOC_MISS_ANCHOR_POINTER, conf,
                   problem_first=(3, 11), problem_second=(6, 11))
        self.check(DUPLICATE_ANCHORS, conf,
                   problem=(5, 15))
