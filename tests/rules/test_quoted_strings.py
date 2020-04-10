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
        self.check('---\n'
                   'bar: "123"\n', conf)

    def test_quote_type_any(self):
        conf = 'quoted-strings: {quote-type: any}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'                          # fails
                   'string2: "foo"\n'
                   'string3: "true"\n'
                   'string4: "123"\n'
                   'string5: \'bar\'\n'
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n',         # fails
                   conf, problem1=(4, 10), problem2=(17, 5),
                   problem3=(19, 12), problem4=(20, 15))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'               # fails
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf, problem1=(9, 3))

    def test_quote_type_single(self):
        conf = 'quoted-strings: {quote-type: single}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'                          # fails
                   'string2: "foo"\n'                        # fails
                   'string3: "true"\n'                       # fails
                   'string4: "123"\n'                        # fails
                   'string5: \'bar\'\n'
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'                             # fails
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n',         # fails
                   conf, problem1=(4, 10), problem2=(5, 10), problem3=(6, 10),
                   problem4=(7, 10), problem5=(17, 5), problem6=(18, 5),
                   problem7=(19, 12), problem8=(19, 17), problem9=(20, 15),
                   problem10=(20, 23))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'               # fails
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf, problem1=(9, 3), problem2=(12, 3))

    def test_quote_type_double(self):
        conf = 'quoted-strings: {quote-type: double}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'                          # fails
                   'string2: "foo"\n'
                   'string3: "true"\n'
                   'string4: "123"\n'
                   'string5: \'bar\'\n'                      # fails
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n',         # fails
                   conf, problem1=(4, 10), problem2=(8, 10), problem3=(17, 5),
                   problem4=(19, 12), problem5=(20, 15))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'               # fails
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf, problem1=(9, 3))

    def test_any_quotes_not_required(self):
        conf = 'quoted-strings: {quote-type: any, required: false}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'
                   'string2: "foo"\n'
                   'string3: "true"\n'
                   'string4: "123"\n'
                   'string5: \'bar\'\n'
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n',         # fails
                   conf)
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
                   conf)

    def test_single_quotes_not_required(self):
        conf = 'quoted-strings: {quote-type: single, required: false}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'
                   'string2: "foo"\n'                        # fails
                   'string3: "true"\n'                       # fails
                   'string4: "123"\n'                        # fails
                   'string5: \'bar\'\n'
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n',         # fails
                   conf, problem1=(5, 10), problem2=(6, 10), problem3=(7, 10),
                   problem4=(18, 5), problem5=(19, 17), problem6=(20, 23))
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
                   '  "word 1\\\n'            # fails
                   '   word 2"\n',
                   conf, problem1=(12, 3))

    def test_only_when_needed(self):
        conf = 'quoted-strings: {required: only-when-needed}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'
                   'string2: "foo"\n'                        # fails
                   'string3: "true"\n'
                   'string4: "123"\n'
                   'string5: \'bar\'\n'                      # fails
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'
                   '  - "foo"\n'                             # fails
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n',         # fails
                   conf, problem1=(5, 10), problem2=(8, 10), problem3=(18, 5),
                   problem4=(19, 17), problem5=(20, 23))
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
                   '  "word 1\\\n'            # fails
                   '   word 2"\n',
                   conf, problem1=(12, 3))

    def test_only_when_needed_single_quotes(self):
        conf = ('quoted-strings: {quote-type: single,\n'
                '                 required: only-when-needed}\n')

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'
                   'string2: "foo"\n'                        # fails
                   'string3: "true"\n'                       # fails
                   'string4: "123"\n'                        # fails
                   'string5: \'bar\'\n'                      # fails
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'
                   '  - "foo"\n'                             # fails
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n',         # fails
                   conf, problem1=(5, 10), problem2=(6, 10), problem3=(7, 10),
                   problem4=(8, 10), problem5=(18, 5), problem6=(19, 17),
                   problem7=(20, 23))
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
                   '  "word 1\\\n'            # fails
                   '   word 2"\n',
                   conf, problem1=(12, 3))
