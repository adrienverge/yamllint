# Copyright (C) 2016 Adrien Vergé
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
Use this rule to control the number of spaces after hyphens (``-``).

.. rubric:: Options

* ``max-spaces-after`` defines the maximal number of spaces allowed after
  hyphens. Set to a negative integer if you want to allow any number of
  spaces.
* ``min-spaces-after`` defines the minimal number of spaces expected after
  hyphens. Set to a negative integer if you want to allow any number of
  spaces. When set to a positive value, cannot be greater than
  ``max-spaces-after``.
* YAMLLint will consider ``-xx`` as a scalar. However you may consider
  that, in your context, such a syntax is a typo and is actually a sequence
  and as a consequence there should be a space after the hyphen. As this is
  not a standard behaviour, you explicitly need to enable this control by
  setting the option ``check-scalars`` to ``true``.  **Use with caution**
  as all scalars will be checked and non-solvable false positive might be
  identified. Has no effect when set to ``true`` but ``min-spaces-after``
  is disabled (< 0).

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   hyphens:
     max-spaces-after: 1
     min-spaces-after: -1  # Disabled
     check-scalars: false

.. rubric:: Examples

#. With ``hyphens: {max-spaces-after: 1}``

   the following code snippet would **PASS**:
   ::

    - first list:
        - a
        - b
    - - 1
      - 2
      - 3

   the following code snippet would **FAIL**:
   ::

    -  first list:
         - a
         - b

   the following code snippet would **FAIL**:
   ::

    - - 1
      -  2
      - 3

#. With ``hyphens: {max-spaces-after: 3}``

   the following code snippet would **PASS**:
   ::

    -   key
    -  key2
    - key42

   the following code snippet would **FAIL**:
   ::

    -    key
    -   key2
    -  key42

#. With ``hyphens: {min-spaces-after: 3}``

   the following code snippet would **PASS**:
   ::

    list:
    -   key
    -    key2
    -     key42
    -foo:  # starter of a new sequence named "-foo";
           # without the colon, a syntax error will be raised.

   the following code snippet would **FAIL**:
   ::

    -  key
    -   key2
    -  key42

#. With ``hyphens: {min-spaces-after: 3, check-scalars: true}``

   the following code snippet would **PASS**:
   ::

    list:
    -   key
    -    key2
    -     key42
    key: -value

   the following code snippets would **FAIL**:
   ::

    ---
    -item0

   ::

    sequence:
      -key  # Mind the spaces before the hyphen to enforce
            # the sequence and avoid a syntax error
"""


import yaml

from yamllint.linter import LintProblem
from yamllint.rules.common import spaces_after


ID = 'hyphens'
TYPE = 'token'
CONF = {'max-spaces-after': int,
        'min-spaces-after': int,
        'check-scalars': bool}
DEFAULT = {'max-spaces-after': 1,
           'min-spaces-after': -1,
           'check-scalars': False}


def VALIDATE(conf):
    if conf['max-spaces-after'] == 0:
        return '"max-spaces-after" cannot be set to 0'
    if (conf['min-spaces-after'] > 0 and
            conf['min-spaces-after'] > conf['max-spaces-after']):
        return '"min-spaces-after" cannot be greater than "max-spaces-after"'


def check(conf, token, prev, next, nextnext, context):
    if isinstance(token, yaml.BlockEntryToken):
        if conf['max-spaces-after'] > 0:
            problem = spaces_after(token, prev, next,
                                   max=conf['max-spaces-after'],
                                   max_desc='too many spaces after hyphen')
            if problem is not None:
                yield problem

        if conf['min-spaces-after'] > 0:
            problem = spaces_after(token, prev, next,
                                   min=conf['min-spaces-after'],
                                   min_desc='too few spaces after hyphen')
            if problem is not None:
                yield problem

    if (conf['check-scalars'] and conf['min-spaces-after'] > 0
            and isinstance(token, yaml.ScalarToken)):
        # Token identified as a scalar so there is no space after the
        # hyphen: no need to count
        if token.value.startswith('-'):
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                'too few spaces after hyphen')
