# -*- coding: utf-8 -*-
# Copyright (C) 2020 Satoru SATOH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# pylint: disable=missing-function-docstring
"""test cases for flow-mapping rule.
"""
import tests.common


class FlowMappingTestCase(tests.common.RuleTestCase):
    """Flow Mapping test cases.
    """
    rule_id = 'flow-mapping'

    def test_disabled(self):
        conf = 'flow-mapping: disable'
        self.check('---\n'
                   '1: {"a": 2}\n', conf)

    def test_enabled(self):
        conf = 'flow-mapping: enable\n'
        self.check('---\n'
                   '1: {"a": 2}\n',
                   conf, problem1=(2, 4))
        self.check('---\n'
                   '1:\n'
                   '  a: 2\n', conf)
        self.check('---\n'
                   '1: {\n'
                   '  "a": 2,\n'
                   '}\n', conf,
                   problem1=(2, 4))
