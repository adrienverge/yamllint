#
# Copyright (C) 2020 Satoru SATOH
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
#
"""
Use this rule to override some comments' rules.

.. rubric:: Options

* Use ``forbid`` to control comments. Set to ``true`` to forbid comments
  completely.

.. rubric:: Examples

#. With ``override-comments: {forbid: true}``

   the following code snippet would **PASS**:
   ::

    foo: 1

   the following code snippet would **FAIL**:
   ::

    # baz
    foo: 1

.. rubric:: Default values (when enabled)

.. code-block:: yaml

rules:
  override-comments:
    forbid: False

"""
from yamllint.linter import LintProblem


ID = 'override-comments'
TYPE = 'comment'
CONF = {'forbid': bool}
DEFAULT = {'forbid': False}


def check(conf, comment):
    """Check if comments are found.
    """
    if conf['forbid']:
        yield LintProblem(comment.line_no, comment.column_no,
                          'forbidden comment')
