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

from tests.common import RuleTestCase


class QuotedTestCase(RuleTestCase):
    rule_id = 'quoted-strings'

    def test_disabled(self):
        conf = 'quoted-strings: disable'
        self.check('---\n'
                   'foo: bar\n', conf)
        self.check('---\n'
                   'foo: "bar"\n', conf)
        self.check('---\n'
                   'foo: \'bar\'\n', conf)
        self.check('---\n'
                   'bar: 123\n', conf)

    def test_quote_type_any(self):
        conf = 'quoted-strings: {quote-type: any}\n'
        self.check('---\n'
                   'string1: "foo"\n'
                   'number1: 123\n'                          # fails
                   'string2: foo\n'                          # fails
                   'string3: \'bar\'\n'
                   'string4: !!str genericstring\n'          # fails
                   'string5: !!str 456\n'                    # fails
                   'string6: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean1: !!bool boolstring\n'
                   'boolean2: !!bool "quotedboolstring"\n',
                   conf, problem1=(3, 10), problem2=(4, 10),
                   problem3=(6, 16), problem4=(7, 16))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf, problem1=(9, 3))

    def test_quote_type_single(self):
        conf = 'quoted-strings: {quote-type: single}\n'
        self.check('---\n'
                   'string1: "foo"\n'                        # fails
                   'number1: 123\n'                          # fails
                   'string2: foo\n'                          # fails
                   'string3: \'bar\'\n'
                   'string4: !!str genericstring\n'          # fails
                   'string5: !!str 456\n'                    # fails
                   'string6: !!str "quotedgenericstring"\n'  # fails
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean1: !!bool boolstring\n'
                   'boolean2: !!bool "quotedboolstring"\n',
                   conf, problem1=(2, 10), problem2=(3, 10), problem3=(4, 10),
                   problem4=(6, 16), problem5=(7, 16), problem6=(8, 16))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf, problem1=(9, 3), problem2=(12, 3))

    def test_quote_type_double(self):
        conf = 'quoted-strings: {quote-type: double}\n'
        self.check('---\n'
                   'string1: "foo"\n'
                   'number1: 123\n'                          # fails
                   'string2: foo\n'                          # fails
                   'string3: \'bar\'\n'                      # fails
                   'string4: !!str genericstring\n'          # fails
                   'string5: !!str 456\n'                    # fails
                   'string6: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean1: !!bool boolstring\n'
                   'boolean2: !!bool "quotedboolstring"\n',
                   conf, problem1=(3, 10), problem2=(4, 10), problem3=(5, 10),
                   problem4=(6, 16), problem5=(7, 16))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf, problem1=(9, 3))
