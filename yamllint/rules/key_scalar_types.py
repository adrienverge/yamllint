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
Use this rule to control the scalar types that are allowed for keys in
mappings.

.. rubric:: Options

* ``allowed`` defines the list of scalar types allowed for keys. The default is
   all standard scalar types, ``[str, int, float, bool, "null", timestamp]``,
   but can be changed to any list containing a subset of these types. Note that
   ``null`` must be quoted.

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   key-scalar-types:
     allowed: [str, int, float, bool, "null", timestamp]

.. rubric:: Examples

#. With ``key-scalar-types: {}``

   the following code snippet would **PASS**:
   ::

    foo: string key
    123: integer key
    1.23: floating point key
    true: boolean key
    null: null key
    2023-10-11: timestamp key

#. With ``key-scalar-types: {allowed: [str]}``

   the following code snippet would **FAIL**:
   ::

    123: integer key
    1.23: floating point key
    true: boolean key
    null: null key
    2023-10-11: timestamp key

   This can be useful to prevent surprises from YAML parsers transforming
   non-string keys into strings, for example when converting to JSON. Some
   common surprises are:

   * ``{010: not ten}`` --> ``{"8": "not ten"}``
   * ``{08: string because not octal}`` -->
     ``{"08": "string because not octal"}``
   * ``{0.0: zero}`` --> ``{"0": "zero"}``
   * ``{9876543210.0123456789: truncated}`` -->
     ``{"9876543210.012346": "truncated"}``
   * ``{True: "True"}`` --> ``{"true": "True"}``
   * ``{Null: "Null"}`` --> ``{"null": "Null"}``
   * ``{2023-10-09: today}`` -->
     ``{"Sun Oct 08 2023 20:00:00 GMT-0400 (Eastern Daylight Time)": "today"}``

   The following code snippet would **PASS**:
   ::

    "010": zero one zero
    "0.0": zero point zero
    "9876543210.0123456789": not truncated
    "True": True (case preserved)
    "Null": Null (case preserved)
    "2023-10-09": Just a string
    foo: string1
    a123: string2
    b{}: string3
    c[]: string4
    v1.23: string5
    08: string6

"""

import yaml

from yamllint.linter import LintProblem
from yamllint.rules.common import is_key

SCALAR_TYPES = ['str',
                'int',
                'float',
                'bool',
                'null',
                'timestamp'
                ]

ID = 'key-scalar-types'
TYPE = 'token'
CONF = {'allowed': SCALAR_TYPES.copy()}
DEFAULT = {'allowed': SCALAR_TYPES}


def VALIDATE(conf):

    key_scalar_types = conf['allowed']
    seen_types = []
    for allowed_type in key_scalar_types:
        if allowed_type is None:
            return 'scalar type "null" must be quoted in "allowed" list'
        if allowed_type in seen_types:
            return f'duplicate scalar type "{allowed_type}" in "allowed" list'
        seen_types.append(allowed_type)


def check(conf, token, prev, next, nextnext, context):
    if not is_key(prev):
        return

    token_type = None
    if isinstance(token, yaml.tokens.TagToken) and (
            token.value[0] == '!!'):  # Explicit type
        token_type = token.value[1]
    elif isinstance(token, yaml.tokens.ScalarToken):
        if token.style:  # if style is quoted, it's a string
            token_type = 'str'
        else:
            resolver = yaml.resolver.Resolver()
            tag = resolver.resolve(yaml.nodes.ScalarNode, token.value,
                                   (True, False))
            token_type = tag.split(':')[-1]

    if token_type not in SCALAR_TYPES:  # unknown type
        return

    if token_type not in conf['allowed']:
        yield LintProblem(
            token.start_mark.line + 1,
            token.start_mark.column + 1,
            f"Scalar type '{token_type}' is not allowed for key nodes")
