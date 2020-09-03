# -*- coding: utf-8 -*-
# Copyright (C) 2020 Satoru SATOH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# pylint: disable=missing-function-docstring
"""test cases for  flow-sequence rule.
"""
import tests.common


class FlowSequenceTestCase(tests.common.RuleTestCase):
    """Flow Sequence test cases.
    """
    rule_id = 'flow-sequence'

    def test_disabled(self):
        conf = 'flow-sequence: disable'
        self.check('---\n'
                   '1: [2, 3]\n', conf)

    def test_enabled(self):
        conf = 'flow-sequence: enable\n'
        self.check('---\n'
                   '1: [2, 3]\n',
                   conf, problem1=(2, 4))
        self.check('---\n'
                   '1:\n'
                   '  - 2\n'
                   '  - 3\n', conf)
        self.check('---\n'
                   '[\n'
                   '  1,\n'
                   '  2\n'
                   ']\n', conf,
                   problem1=(2, 1))
