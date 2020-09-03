#
# Copyright (C) 2020 Satoru SATOH
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Use this rule to forbid flow sequences of which content is denoted by
surrounding "[" and "]".

.. rubric:: Examples

#. The following code snippet would **PASS**:
   ::

    foo:
      - bar
      - baz

#. The following code snippet would **FAIL**:
   ::

    foo: ['bar', 'baz']

"""
import yaml

from yamllint.linter import LintProblem


ID = 'flow-sequence'
TYPE = 'token'


def check(conf, token, _prev, _next, _nextnext, _context):
    """Check if the toke starts flow sequnce is found.
    """
    if isinstance(token, yaml.FlowSequenceStartToken):
        yield LintProblem(token.start_mark.line + 1,
                          token.start_mark.column + 1,
                          "Flow Sequences are forbidden.")
