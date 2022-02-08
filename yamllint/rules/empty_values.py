# -*- coding: utf-8 -*-
# Copyright (C) 2017 Greg Dubicki
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
Use this rule to prevent nodes with empty content, that implicitly result in
``null`` values.

.. rubric:: Options

* Use ``forbid-in-block-mappings`` to prevent empty values in block mappings.
* Use ``forbid-in-flow-mappings`` to prevent empty values in flow mappings.
* Use ``forbid-key-without-values-eof`` to prevent empty values at the end of a file.

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   empty-values:
     forbid-in-block-mappings: true
     forbid-in-flow-mappings: true
     forbid-key-without-values-eof: false

.. rubric:: Examples

#. With ``empty-values: {forbid-in-block-mappings: true}``

   the following code snippets would **PASS**:
   ::

    some-mapping:
      sub-element: correctly indented

   ::

    explicitly-null: null

   the following code snippets would **FAIL**:
   ::

    some-mapping:
    sub-element: incorrectly indented

   ::

    implicitly-null:

#. With ``empty-values: {forbid-in-flow-mappings: true}``

   the following code snippet would **PASS**:
   ::

    {prop: null}
    {a: 1, b: 2, c: 3}

   the following code snippets would **FAIL**:
   ::

    {prop: }

   ::

    {a: 1, b:, c: 3}

#. With ``empty-values: {forbid-key-without-values-eof: true}``

   the following code snippet would **PASS**:
   ::

    key: value

   the following code snippet would **FAIL**:
   ::

    key:value

"""

import yaml

from yamllint.linter import LintProblem


ID = 'empty-values'
TYPE = 'token'
CONF = {'forbid-in-block-mappings': bool,
        'forbid-in-flow-mappings': bool,
        'forbid-key-without-values-eof': bool}
DEFAULT = {'forbid-in-block-mappings': True,
           'forbid-in-flow-mappings': True,
           'forbid-key-without-values-eof': False}


def check(conf, token, prev, next, nextnext, context):
    if conf['forbid-in-block-mappings']:
        if isinstance(token, yaml.ValueToken) and isinstance(next, (
                yaml.KeyToken, yaml.BlockEndToken)):
            yield LintProblem(token.start_mark.line + 1,
                              token.end_mark.column + 1,
                              'empty value in block mapping')

    if conf['forbid-in-flow-mappings']:
        if isinstance(token, yaml.ValueToken) and isinstance(next, (
                yaml.FlowEntryToken, yaml.FlowMappingEndToken)):
            yield LintProblem(token.start_mark.line + 1,
                              token.end_mark.column + 1,
                              'empty value in flow mapping')

    if conf['forbid-key-without-values-eof']:
        if isinstance(prev, (yaml.KeyToken, yaml.DocumentStartToken,
                             yaml.StreamStartToken)) \
                and isinstance(token, yaml.ScalarToken) \
                and isinstance(next, (yaml.DocumentEndToken,
                                      yaml.StreamEndToken)):
            yield LintProblem(token.start_mark.line + 1,
                              token.end_mark.column + 1,
                              'key with no value found')
