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
Use this rule to forbid any values that are not quoted. You can also enforce
the type of the quote used - single or double.

.. rubric:: Examples

#. With ``quoted: {quote-type: any}``

   the following code snippet would **PASS**:
   ::

    foo: "bar"
    bar: 'foo'

   the following code snippet would **FAIL**:
   ::

    foo: bar
    bar: 123
"""

import yaml

from yamllint.linter import LintProblem

ID = 'quoted'
TYPE = 'token'
CONF = {'quote-type': ('any', 'single', 'double')}


def check(conf, token, prev, next, nextnext, context):
    if prev and isinstance(prev, yaml.tokens.TagToken):
        return

    if isinstance(token, yaml.tokens.ScalarToken):

        if isinstance(prev, yaml.tokens.ValueToken):
            quote_type = conf['quote-type']
            if ((quote_type == 'single' and token.style != "'") or
                    (quote_type == 'double' and token.style != '"') or
                    (quote_type == 'any' and token.style is None)):
                yield LintProblem(
                    token.start_mark.line + 1,
                    token.start_mark.column + 1,
                    "value is not quoted (using %s quote)" % quote_type
                )
