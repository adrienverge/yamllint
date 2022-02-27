# Copyright (C) 2022 Sergei Mikhailov
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
Use this rule to prevent duplicated anchors and referencing to non-existent anchors.

.. rubric:: Options

* Use ``forbid-unknown-aliases`` to prevent referencing to anchors before assigment or referencing to non-existent anchors.
* Use ``forbid-duplicated-anchors`` to prevent duplicated anchors.


.. rubric:: Examples

#. With ``anchors: {forbid-duplicated-anchors: true}``

   the following code snippet would **PASS**:
   ::

    clients:
        jack: &jack_client
            billing_id: 1234
        bill: &bill_client
            billing_id: 5678
    target_client: *jack_client

   the following code snippet would **FAIL**:
   ::

    clients:
        jack: &jack_client
            billing_id: 1234
        bill: &jack_client
            billing_id: 5678
    target_client: *jack_client

#. With ``anchors: {forbid-unknown-aliases: true}``

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


from yaml import StreamStartToken, DocumentStartToken, AnchorToken, AliasToken

from yamllint.linter import LintProblem


ID = 'anchors'
TYPE = 'token'

CONF = {'forbid-unknown-aliases': bool,
        'forbid-duplicated-anchors': bool}
DEFAULT = {'forbid-unknown-aliases': True,
           'forbid-duplicated-anchors': False}


def check(conf, token, prev, next, nextnext, context):
    if conf['forbid-unknown-aliases'] or conf['forbid-duplicated-anchors']:
        # In case of DocumentStartToken `---` is missing
        if isinstance(token, StreamStartToken):
            context['anchors'] = []
        if isinstance(token, DocumentStartToken):
            context['anchors'] = []
        elif isinstance(token, AnchorToken):
            context['anchors'].append(token.value)

    if conf['forbid-unknown-aliases'] and isinstance(token, AliasToken):
        if token.value not in context['anchors']:
            yield LintProblem(
                token.start_mark.line + 1, token.start_mark.column + 1,
                f'anchor "{token.value}" is used before assignment')


    if conf['forbid-duplicated-anchors'] and isinstance(token, AnchorToken):
        anchors_count = context['anchors'].count(token.value)
        if anchors_count == 2:
            yield LintProblem(
                token.start_mark.line + 1, token.start_mark.column + 1,
                f'duplicated anchor "{token.value}')
