# Copyright (C) 2021 Sergei Mikhailov
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
Use this rule to prevent aliases pointing to pointers that don't exist.

.. rubric:: Examples

#. With ``unknown-aliases: {}``

   the following code snippet would **PASS**:
   ::

    address: &address |
      Williams St. 13
    target_address: *address

   the following code snippet would **PASS**:
   ::

    default_address: &address
      state: South Carolina
      city:  Barnwell
    target_address:
      <<: *address
      city: Barnaul

   the following code snippet would **FAIL**:
   ::

    address: &address |
      Williams St. 13
    target_address: *wrong_address


   the following code snippet would **FAIL**:
   ::

    default_address: &address
      state: South Carolina
      city:  Barnwell
    target_address:
      <<: *wrong_address
      city: Barnaul
"""

from yaml import DocumentStartToken, AnchorToken, AliasToken

from yamllint.linter import LintProblem


ID = 'unknown-aliases'
TYPE = 'token'

CONF = {'unknown-aliases': bool}
DEFAULT = {'unknown-aliases': True}


def check(conf, token, __prev, __next, __nextnext, context):
    if conf['unknown-aliases']:
        if isinstance(token, DocumentStartToken):
            context['anchors'] = []
        elif 'anchors' in context:
            if isinstance(token, AnchorToken):
                context['anchors'].append(token.value)
            elif isinstance(token, AliasToken):
                if token.value not in context['anchors']:
                    yield LintProblem(
                        token.start_mark.line + 1, token.start_mark.column + 1,
                        f'anchor "{token.value}" is used before assignment')
