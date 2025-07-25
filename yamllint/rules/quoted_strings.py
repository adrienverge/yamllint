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
* ``extra-required`` is a list of PCRE regexes to force string values to be
  quoted, if they match any regex. This option can only be used with
  ``required: false`` and  ``required: only-when-needed``.
* ``extra-allowed`` is a list of PCRE regexes to allow quoted string values,
  even if ``required: only-when-needed`` is set.
* ``allow-quoted-quotes`` allows (``true``) using disallowed quotes for strings
  with allowed quotes inside. Default ``false``.
* ``check-keys`` defines whether to apply the rules to keys in mappings. By
  default, ``quoted-strings`` rules apply only to values. Set this option to
  ``true`` to apply the rules to keys as well.

**Note**: Multi-line strings (with ``|`` or ``>``) will not be checked.

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   quoted-strings:
     quote-type: any
     required: true
     extra-required: []
     extra-allowed: []
     allow-quoted-quotes: false
     check-keys: false

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

#. With ``quoted-strings: {required: false, extra-required: [^http://,
   ^ftp://]}``

   the following code snippet would **PASS**:
   ::

    - localhost
    - "localhost"
    - "http://localhost"
    - "ftp://localhost"

   the following code snippet would **FAIL**:
   ::

    - http://localhost
    - ftp://localhost

#. With ``quoted-strings: {required: only-when-needed, extra-allowed:
   [^http://, ^ftp://], extra-required: [QUOTED]}``

   the following code snippet would **PASS**:
   ::

    - localhost
    - "http://localhost"
    - "ftp://localhost"
    - "this is a string that needs to be QUOTED"

   the following code snippet would **FAIL**:
   ::

    - "localhost"
    - this is a string that needs to be QUOTED

#. With ``quoted-strings: {quote-type: double, allow-quoted-quotes: false}``

   the following code snippet would **PASS**:
   ::

    foo: "bar\\"baz"

   the following code snippet would **FAIL**:
   ::

    foo: 'bar"baz'

#. With ``quoted-strings: {quote-type: double, allow-quoted-quotes: true}``

   the following code snippet would **PASS**:
   ::

    foo: 'bar"baz'

#. With ``quoted-strings: {required: only-when-needed, check-keys: true,
   extra-required: ["[:]"]}``

   the following code snippet would **FAIL**:
   ::

    foo:bar: baz

   the following code snippet would **PASS**:
   ::

    "foo:bar": baz
"""

import re

import yaml

from yamllint.linter import LintProblem

ID = 'quoted-strings'
TYPE = 'token'
CONF = {'quote-type': ('any', 'single', 'double'),
        'required': (True, False, 'only-when-needed'),
        'extra-required': [str],
        'extra-allowed': [str],
        'allow-quoted-quotes': bool,
        'check-keys': bool}
DEFAULT = {'quote-type': 'any',
           'required': True,
           'extra-required': [],
           'extra-allowed': [],
           'allow-quoted-quotes': False,
           'check-keys': False}


def VALIDATE(conf):
    if conf['required'] is True and len(conf['extra-allowed']) > 0:
        return 'cannot use both "required: true" and "extra-allowed"'
    if conf['required'] is True and len(conf['extra-required']) > 0:
        return 'cannot use both "required: true" and "extra-required"'
    if conf['required'] is False and len(conf['extra-allowed']) > 0:
        return 'cannot use both "required: false" and "extra-allowed"'


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


def _quote_match(quote_type, token_style):
    return ((quote_type == 'any') or
            (quote_type == 'single' and token_style == "'") or
            (quote_type == 'double' and token_style == '"'))


def _quotes_are_needed(token, is_inside_a_flow):
    # Quotes needed on strings containing flow tokens
    if is_inside_a_flow and set(token.value) & {',', '[', ']', '{', '}'}:
        return True

    if token.style == '"':
        try:
            yaml.reader.Reader('').check_printable('key: ' + token.value)
        except yaml.reader.ReaderError:
            # Special characters in a double-quoted string are assumed to have
            # been backslash-escaped
            return True

        if _has_backslash_on_at_least_one_line_ending(token):
            return True

    loader = yaml.BaseLoader('key: ' + token.value)
    # Remove the 5 first tokens corresponding to 'key: ' (StreamStartToken,
    # BlockMappingStartToken, KeyToken, ScalarToken(value=key), ValueToken)
    for _ in range(5):
        loader.get_token()
    try:
        a, b = loader.get_token(), loader.get_token()
    except yaml.scanner.ScannerError:
        return True
    else:
        if (isinstance(a, yaml.ScalarToken) and a.style is None and
                isinstance(b, yaml.BlockEndToken) and a.value == token.value):
            return False
        return True


def _has_quoted_quotes(token):
    return ((not token.plain) and
            ((token.style == "'" and '"' in token.value) or
             (token.style == '"' and "'" in token.value)))


def _has_backslash_on_at_least_one_line_ending(token):
    if token.start_mark.line == token.end_mark.line:
        return False
    buffer = token.start_mark.buffer[
        token.start_mark.index + 1:token.end_mark.index - 1]
    return '\\\n' in buffer or '\\\r\n' in buffer


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

    node = 'key' if isinstance(prev, yaml.KeyToken) else 'value'
    if node == 'key' and not conf['check-keys']:
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
    if not token.plain and token.style in ("|", ">"):
        return

    quote_type = conf['quote-type']

    msg = None
    if conf['required'] is True:

        # Quotes are mandatory and need to match config
        if (token.style is None or
            not (_quote_match(quote_type, token.style) or
                 (conf['allow-quoted-quotes'] and _has_quoted_quotes(token)))):
            msg = f"string {node} is not quoted with {quote_type} quotes"

    elif conf['required'] is False:

        # Quotes are not mandatory but when used need to match config
        if (token.style and
                not _quote_match(quote_type, token.style) and
                not (conf['allow-quoted-quotes'] and
                     _has_quoted_quotes(token))):
            msg = f"string {node} is not quoted with {quote_type} quotes"

        elif not token.style:
            is_extra_required = any(re.search(r, token.value)
                                    for r in conf['extra-required'])
            if is_extra_required:
                msg = f"string {node} is not quoted"

    elif conf['required'] == 'only-when-needed':

        # Quotes are not strictly needed here
        if (token.style and tag == DEFAULT_SCALAR_TAG and token.value and
                not _quotes_are_needed(token, context['flow_nest_count'] > 0)):
            is_extra_required = any(re.search(r, token.value)
                                    for r in conf['extra-required'])
            is_extra_allowed = any(re.search(r, token.value)
                                   for r in conf['extra-allowed'])
            if not (is_extra_required or is_extra_allowed):
                msg = (f"string {node} is redundantly quoted with "
                       f"{quote_type} quotes")

        # But when used need to match config
        elif (token.style and
              not _quote_match(quote_type, token.style) and
              not (conf['allow-quoted-quotes'] and _has_quoted_quotes(token))):
            msg = f"string {node} is not quoted with {quote_type} quotes"

        elif not token.style:
            is_extra_required = len(conf['extra-required']) and any(
                re.search(r, token.value) for r in conf['extra-required'])
            if is_extra_required:
                msg = f"string {node} is not quoted"

    if msg is not None:
        yield LintProblem(
            token.start_mark.line + 1,
            token.start_mark.column + 1,
            msg)
