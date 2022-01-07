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
Use this rule to forbid duplicated anchors.

.. rubric:: Examples

#. With ``anchor-duplicates: {}``

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
"""

from yaml import DocumentStartToken, AnchorToken, AliasToken

from yamllint.linter import LintProblem


ID = 'anchor-duplicates'
TYPE = 'token'

CONF = {'anchor-duplicates': bool}
DEFAULT = {'anchor-duplicates': True}

def check(conf, token, __prev, __next, __nextnext, context):
    if conf['anchor-duplicates']:
        if isinstance(token, DocumentStartToken):
            context['anchors'] = []
        elif 'anchors' in context:
            if isinstance(token, AnchorToken):
                if token.value in context['anchors']:
                    yield LintProblem(
                        token.start_mark.line + 1, token.start_mark.column + 1,
                        f'duplicated anchor "{token.value}"')
                context['anchors'].append(token.value)
