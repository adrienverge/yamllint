# -*- coding: utf-8 -*-
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

#. With ``anchors: {}``

   the following code snippet would **PASS**:
   ::

    address: &address |
      Williams St. 13
    target_address: *address

   the following code snippet would **FAIL**:
   ::

    address: &address |
      Williams St. 13
    target_address: *wrong_address

#. This appends to merges as well:

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

    default_address: &address
      state: South Carolina
      city:  Barnwell
    target_address:
      <<: *wrong_address
      city: Barnaul

#. Duplicate anchors are not allowed.

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

from yaml import DocumentStartToken, AnchorToken, AliasToken, BlockEndToken

from yamllint.linter import LintProblem


ID = 'anchors'
TYPE = 'token'


def check(__conf, token, __prev, __next, __nextnext, context):
    if isinstance(token, (DocumentStartToken)):
        context['anchors'] = set()
        context['aliases'] = {}
    elif ('anchors' in context and 'aliases' in context):
        if isinstance(token, (AnchorToken)):
            if token.value in context['anchors']:
                yield LintProblem(
                    token.start_mark.line + 1, token.start_mark.column + 1,
                    f"anchor '{token.value}' duplicates in document")
            context['anchors'].add(token.value)
        elif isinstance(token, (AliasToken)):
            if token.value not in context['aliases']:
                context['aliases'][token.value] = []
            alias_obj = {"line": token.start_mark.line,
                         "column": token.start_mark.column}
            context['aliases'][token.value].append(alias_obj)
        elif isinstance(token, (BlockEndToken)):
            missing_anchors = [alias for alias in list(context['aliases'])
                               if alias not in context['anchors']]
            if len(missing_anchors) > 0:
                for miss_anchor in missing_anchors:
                    for location in context['aliases'][miss_anchor]:
                        yield LintProblem(
                            location['line'] + 1, location['column'] + 1,
                            f"anchor '{miss_anchor}' is not found in document")
