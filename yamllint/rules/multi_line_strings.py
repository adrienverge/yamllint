# Copyright (C) 2024 Arm, Ltd.
# Based on quoted_strings.py, Copyright (C) 2018 ClearScore
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
Use this rule to check if multi-line strings formatting matches the token
used for the text block.

.. rubric:: Options

* ``missing-block-token`` defines whether to check if a multi-line string needs
  a literal or folded token to preserve its formatting.
* ``unnecessary-block-token`` defines whether ...

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   multi-line-strings:
     missing-block-token: true
     unnecessary-block-token: true

.. rubric:: Examples

#. With ``multi-line-strings: {missing-block-token: true}``

   the following code snippet would **PASS**:
   ::

    foo:
      bar
      baz

   the following code snippet would **FAIL**:
   ::

    foo:
      bar

      baz

#. With ``multi-line-strings: {unnecessary-block-token: true}``

   the following code snippet would **PASS**:
   ::

    foo: |
      bar

      baz

   the following code snippet would **FAIL**:
   ::

    foo: |
      bar
      baz

"""

import re

import yaml

from yamllint.linter import LintProblem

ID = 'multi-line-strings'
TYPE = 'token'
CONF = {'missing-block-token': bool,
        'unnecessary-block-token': (True, False, 'folded', 'block')}
DEFAULT = {'missing-block-token': False,
           'unnecessary-block-token': False}

DEFAULT_SCALAR_TAG = 'tag:yaml.org,2002:str'

# https://stackoverflow.com/a/36514274
yaml.resolver.Resolver.add_implicit_resolver(
    'tag:yaml.org,2002:int',
    re.compile(r'''^(?:[-+]?0b[0-1_]+
               |[-+]?0o?[0-7_]+
               |[-+]?0[0-7_]+
               |[-+]?(?:0|[1-9][0-9_]*)
               |[-+]?0x[0-9a-fA-F_]+
               |[-+]?[1-9][0-9_]*(?::[0-5]?[0-9])+)$''', re.VERBOSE),
    list('-+0123456789'))


def check(conf, token, prev, next, nextnext, context):
    if 'flow_nest_count' not in context:
        context['flow_nest_count'] = 0

    if isinstance(token, (yaml.FlowMappingStartToken,
                          yaml.FlowSequenceStartToken)):
        context['flow_nest_count'] += 1
    elif isinstance(token, (yaml.FlowMappingEndToken,
                            yaml.FlowSequenceEndToken)):
        context['flow_nest_count'] -= 1

    if not (isinstance(token, yaml.tokens.ScalarToken) and
            isinstance(prev, (yaml.BlockEntryToken, yaml.FlowEntryToken,
                              yaml.FlowSequenceStartToken, yaml.TagToken,
                              yaml.ValueToken, yaml.KeyToken))):
        return

    if isinstance(prev, yaml.KeyToken):
        return

    # Ignore explicit types, e.g. !!str testtest or !!int 42
    if (prev and isinstance(prev, yaml.tokens.TagToken) and
            prev.value[0] == '!!'):
        return

    # Ignore numbers, booleans, etc.
    resolver = yaml.resolver.Resolver()
    tag = resolver.resolve(yaml.nodes.ScalarNode, token.value, (True, False))
    if token.plain and tag != DEFAULT_SCALAR_TAG:
        return

    msg = None
    if conf['unnecessary-block-token'] and token.style in ("|", ">"):
        if conf['unnecessary-block-token'] == 'folded' and token.style != '>':
            return
        elif conf['unnecessary-block-token'] == 'block' and token.style != '|':
            return
        value = token.value.rstrip('\n')
        if value[0] in "\n#>|'\"&*!{}[]@%":
            return
        if token.style == '>' and "\n" in value:
            return
        if '\n\n' in value or '\n ' in value:
            return
        if ': ' in value or ':\n' in value or ' #' in value:
            return
        msg = (
            f"unnecessary '{token.style}' block token for string value"
            f" '{token.value[:40]}...'"
        )
    elif conf['missing-block-token'] and token.plain:
        # Need the raw lines, otherwise any formatting got stripped out
        lines = token.start_mark.buffer.splitlines()
        lines = lines[token.start_mark.line:(token.end_mark.line + 1)]
        if ': ' in lines[0] and len(lines) > 1:
            lines = lines[1:]
        indent = len(lines[0]) - len(lines[0].lstrip(' '))
        for line in lines:
            if len(line) == 0 or len(line) > indent and line[indent] == ' ':
                msg = (
                    f"formatting in string value '{token.value[:40]}...' "
                    f"needs block('|') or folded('>') token"
                )
                break

    if msg is not None:
        yield LintProblem(
            token.start_mark.line + 1,
            token.start_mark.column + 1,
            msg)
