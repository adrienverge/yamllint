# -*- coding: utf-8 -*-
# Copyright (C) 2016 Peter Ericson
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

"""
Use this rule to forbid truthy values that are not quoted nor explicitly typed.

This would prevent YAML parsers to tranform ``[yes, FALSE, Off]`` into ``[true,
false, false]`` or ``{y: 1, yes: 2, on: 3, true: 4, True: 5}`` into ``{y: 1,
true: 5}``.

.. rubric:: Examples

#. With ``truthy: {}``

   the following code snippet would **PASS**:
   ::

    boolean: true

    object: {"True": 1, 1: "True"}

    "yes":  1
    "on":   2
    "true": 3
    "True": 4

     explicit:
       string1: !!str True
       string2: !!str yes
       string3: !!str off
       encoded: !!binary |
                  True
                  OFF
                  pad==  # this decodes as 'N\xbb\x9e8Qii'
       boolean1: !!bool true
       boolean2: !!bool "false"
       boolean3: !!bool FALSE
       boolean4: !!bool True
       boolean5: !!bool off
       boolean6: !!bool NO

   the following code snippet would **FAIL**:
   ::

    object: {True: 1, 1: True}

   the following code snippet would **FAIL**:
   ::

    yes:  1
    on:   2
    true: 3
    True: 4
"""

import yaml

from yamllint.linter import LintProblem

ID = 'truthy'
TYPE = 'token'
CONF = {}

TRUTHY = ['YES', 'Yes', 'yes',
          'NO', 'No', 'no',
          'TRUE', 'True',  # 'true' is a boolean
          'FALSE', 'False',  # 'false' is a boolean
          'ON', 'On', 'on',
          'OFF', 'Off', 'off']


def check(conf, token, prev, next, nextnext, context):
    if prev and isinstance(prev, yaml.tokens.TagToken):
        return

    if isinstance(token, yaml.tokens.ScalarToken):
        if token.value in TRUTHY and token.style is None:
            yield LintProblem(token.start_mark.line + 1,
                              token.start_mark.column + 1,
                              "truthy value is not quoted")
