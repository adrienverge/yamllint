#
# Copyright (C) 2020 Satoru SATOH
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Use this rule to forbid flow mappings of which content is denoted by
surrounding "{" and "}".

.. rubric:: Examples

#. The following code snippet would **PASS**:
   ::

    foo:
      bar: 1
    baz:
      a: b

#. The following code snippet would **FAIL**:
   ::

    foo: {'bar': 1}
    baz: {
      'a': 'b'
    }
"""
import yaml

from yamllint.linter import LintProblem


ID = 'flow-mapping'
TYPE = 'token'


def check(conf, token, _prev, _next, _nextnext, _context):
    """Check if the toke starts flow mapping is found.
    """
    if isinstance(token, yaml.FlowMappingStartToken):
        yield LintProblem(token.start_mark.line + 1,
                          token.start_mark.column + 1,
                          "Flow mappings are forbidden.")
