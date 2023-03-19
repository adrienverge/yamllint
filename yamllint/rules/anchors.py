# Copyright (C) 2023 Adrien Vergé
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
Use this rule to report duplicated anchors and aliases referencing undeclared
anchors.

.. rubric:: Options

* Set ``forbid-undeclared-aliases`` to ``true`` to avoid aliases that reference
  an anchor that hasn't been declared (either not declared at all, or declared
  later in the document).
* Set ``forbid-duplicated-anchors`` to ``true`` to avoid duplications of a same
  anchor.

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   anchors:
     forbid-undeclared-aliases: true
     forbid-duplicated-anchors: false

.. rubric:: Examples

#. With ``anchors: {forbid-undeclared-aliases: true}``

   the following code snippet would **PASS**:
   ::

    ---
    - &anchor
      foo: bar
    - *anchor

   the following code snippet would **FAIL**:
   ::

    ---
    - &anchor
      foo: bar
    - *unknown

   the following code snippet would **FAIL**:
   ::

    ---
    - &anchor
      foo: bar
    - <<: *unknown
      extra: value

#. With ``anchors: {forbid-duplicated-anchors: true}``

   the following code snippet would **PASS**:
   ::

    ---
    - &anchor1 Foo Bar
    - &anchor2 [item 1, item 2]

   the following code snippet would **FAIL**:
   ::

    ---
    - &anchor Foo Bar
    - &anchor [item 1, item 2]
"""


import yaml

from yamllint.linter import LintProblem


ID = 'anchors'
TYPE = 'token'
CONF = {'forbid-undeclared-aliases': bool,
        'forbid-duplicated-anchors': bool}
DEFAULT = {'forbid-undeclared-aliases': True,
           'forbid-duplicated-anchors': False}


def check(conf, token, prev, next, nextnext, context):
    if conf['forbid-undeclared-aliases'] or conf['forbid-duplicated-anchors']:
        if isinstance(token, (yaml.StreamStartToken, yaml.DocumentStartToken)):
            context['anchors'] = set()

    if (conf['forbid-undeclared-aliases'] and
            isinstance(token, yaml.AliasToken) and
            token.value not in context['anchors']):
        yield LintProblem(
            token.start_mark.line + 1, token.start_mark.column + 1,
            f'found undeclared alias "{token.value}"')

    if (conf['forbid-duplicated-anchors'] and
            isinstance(token, yaml.AnchorToken) and
            token.value in context['anchors']):
        yield LintProblem(
            token.start_mark.line + 1, token.start_mark.column + 1,
            f'found duplicated anchor "{token.value}"')

    if conf['forbid-undeclared-aliases'] or conf['forbid-duplicated-anchors']:
        if isinstance(token, yaml.AnchorToken):
            context['anchors'].add(token.value)
