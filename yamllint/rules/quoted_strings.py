# -*- coding: utf-8 -*-
# Copyright (C) 2018 ClearScore
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
Use this rule to forbid any string values that are not quoted, or to prevent
quoted strings without needing it. You can also enforce the type of the quote
used.

.. rubric:: Options

* ``quote-type`` defines allowed quotes: ``single``, ``double`` or ``any``
  (default).
* ``required`` defines whether using quotes in string values is required
  (``true``, default) or not (``false``), or only allowed when really needed
  (``only-when-needed``).

**Note**: Multi-line strings (with ``|`` or ``>``) will not be checked.

.. rubric:: Examples

#. With ``quoted-strings: {quote-type: any, required: true}``

   the following code snippet would **PASS**:
   ::

    foo: "bar"
    bar: 'foo'
    number: 123
    boolean: true

   the following code snippet would **FAIL**:
   ::

    foo: bar

#. With ``quoted-strings: {quote-type: single, required: only-when-needed}``

   the following code snippet would **PASS**:
   ::

    foo: bar
    bar: foo
    not_number: '123'
    not_boolean: 'true'
    not_comment: '# comment'
    not_list: '[1, 2, 3]'
    not_map: '{a: 1, b: 2}'

   the following code snippet would **FAIL**:
   ::

    foo: 'bar'
"""

import yaml

from yamllint.linter import LintProblem

ID = 'quoted-strings'
TYPE = 'token'
CONF = {'quote-type': ('any', 'single', 'double'),
        'required': (True, False, 'only-when-needed')}
DEFAULT = {'quote-type': 'any',
           'required': True}

DEFAULT_SCALAR_TAG = u'tag:yaml.org,2002:str'
START_TOKENS = {'#', '*', '!', '?', '@', '`', '&',
                ',', '-', '{', '}', '[', ']', ':'}


def quote_match(quote_type, token_style):
    return ((quote_type == 'any') or
            (quote_type == 'single' and token_style == "'") or
            (quote_type == 'double' and token_style == '"'))


def check(conf, token, prev, next, nextnext, context):
    if not (isinstance(token, yaml.tokens.ScalarToken) and
            isinstance(prev, (yaml.BlockEntryToken, yaml.FlowEntryToken,
                              yaml.FlowSequenceStartToken, yaml.TagToken,
                              yaml.ValueToken))):

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

    # Ignore multi-line strings
    if (not token.plain) and (token.style == "|" or token.style == ">"):
        return

    quote_type = conf['quote-type']
    required = conf['required']

    # Completely relaxed about quotes (same as the rule being disabled)
    if required is False and quote_type == 'any':
        return

    msg = None
    if required is True:

        # Quotes are mandatory and need to match config
        if token.style is None or not quote_match(quote_type, token.style):
            msg = "string value is not quoted with %s quotes" % (quote_type)

    elif required is False:

        # Quotes are not mandatory but when used need to match config
        if token.style and not quote_match(quote_type, token.style):
            msg = "string value is not quoted with %s quotes" % (quote_type)

    elif not token.plain:

        # Quotes are disallowed when not needed
        if (tag == DEFAULT_SCALAR_TAG and token.value
                and token.value[0] not in START_TOKENS):
            msg = "string value is redundantly quoted with %s quotes" % (
                quote_type)

        # But when used need to match config
        elif token.style and not quote_match(quote_type, token.style):
            msg = "string value is not quoted with %s quotes" % (quote_type)

    if msg is not None:
        yield LintProblem(
            token.start_mark.line + 1,
            token.start_mark.column + 1,
            msg)
