# Copyright (C) 2023 Henry Gessau
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
Use this rule to control the kinds of nodes (https://yaml.org/spec/1.2.2/#nodes)
that can be used for keys in mappings.

.. rubric:: Options

* ``allow-mapping`` defines whether mapping nodes are allowed (``true``)
  or not (``false``, default).
* ``allow-sequence`` defines whether sequence nodes are allowed (``true``)
  or not (``false``, default).
* ``allow-scalar`` defines whether scalar nodes are allowed (``true``, default)
  or not (``false``).

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   key-node-kinds:
     allow-mapping: false
     allow-sequence: false
     allow-scalar: true

.. rubric:: Examples

#. With ``key-node-kinds: {}``

   the following code snippet would **PASS**:
   ::

    foo: scalar string key
    123: scalar integer key
    1.23: scalar floating point key
    true: scalar boolean key
    null: scalar null key
    2023-10-11: scalar timestamp key

   the following code snippet would **FAIL**:
   ::

    {foo: bar}: mapping key
    [foo, bar]: sequence key

#. With ``key-node-kinds: {allow-mapping: true}``

   the following code snippet would **PASS**:
   ::

    {foo: bar}: mapping key

#. With ``key-node-kinds: {allow-sequence: true}``

   the following code snippet would **PASS**:
   ::

    [foo, bar]: sequence key

"""

import yaml

from yamllint.linter import LintProblem
from yamllint.rules.common import is_key
from yamllint.rules.key_scalar_types import SCALAR_TYPES

ID = 'key-node-kinds'
TYPE = 'token'
CONF = {'allow-mapping': (True, False),
        'allow-sequence': (True, False),
        'allow-scalar': (True, False)
        }
DEFAULT = {'allow-mapping': False,
           'allow-sequence': False,
           'allow-scalar': True
           }


def check(conf, token, prev, next, nextnext, context):
    if not is_key(prev):
        return

    allow_mapping = conf['allow-mapping']
    if not allow_mapping:
        if isinstance(token, (yaml.tokens.BlockMappingStartToken,
                              yaml.tokens.FlowMappingStartToken)):
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                "Key must not be a mapping")

    allow_sequence = conf['allow-sequence']
    if not allow_sequence:
        if isinstance(token, (yaml.tokens.BlockSequenceStartToken,
                              yaml.tokens.FlowSequenceStartToken)):
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                "Key must not be a sequence")

    allow_scalar = conf['allow-scalar']
    if not allow_scalar:
        if isinstance(token, yaml.tokens.ScalarToken):
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                "Key must not be a scalar")
        elif isinstance(token, yaml.tokens.TagToken) and \
                token.value[0] == '!!' and (token.value[1] in SCALAR_TYPES):
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                "Key explicit type must not be a scalar")
