# Copyright (C) 2023 Jason Yundt
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

import codecs
import itertools
import unittest

from tests.common import (
    encoding_detectable,
    is_test_codec,
    register_test_codecs,
    temp_workspace,
    test_codec_built_in_equivalent,
    unregister_test_codecs,
    uses_bom,
    utf_codecs,
    ws_with_files_in_many_codecs,
)

from yamllint import decoder

test_strings = (
    "",
    "y",
    "yaml",
    "🇾⁠🇦⁠🇲⁠🇱⁠❗"
)
setUpModule = register_test_codecs
tearDownModule = unregister_test_codecs


class EncodingStuffFromCommonTestCase(unittest.TestCase):
    def test_test_codecs_and_utf_codecs(self):
        error = "{} failed to correctly encode then decode {}."
        for string in test_strings:
            for codec in utf_codecs():
                self.assertEqual(
                    string,
                    string.encode(codec).decode(codec),
                    msg=error.format(repr(codec), repr(string))
                )

    def test_is_test_codec(self):
        self.assertFalse(is_test_codec('utf_32'))
        self.assertFalse(is_test_codec('utf_32_be'))
        self.assertTrue(is_test_codec('utf_32_be_sig'))
        self.assertFalse(is_test_codec('utf_32_le'))
        self.assertTrue(is_test_codec('utf_32_le_sig'))

        self.assertFalse(is_test_codec('utf_16'))
        self.assertFalse(is_test_codec('utf_16_be'))
        self.assertTrue(is_test_codec('utf_16_be_sig'))
        self.assertFalse(is_test_codec('utf_16_le'))
        self.assertTrue(is_test_codec('utf_16_le_sig'))

        self.assertFalse(is_test_codec('utf_8'))
        self.assertFalse(is_test_codec('utf_8_be'))

    def test_test_codec_built_in_equivalent(self):
        self.assertEqual(
            'utf_32',
            test_codec_built_in_equivalent('utf_32_be_sig')
        )
        self.assertEqual(
            'utf_32',
            test_codec_built_in_equivalent('utf_32_le_sig')
        )

        self.assertEqual(
            'utf_16',
            test_codec_built_in_equivalent('utf_16_be_sig')
        )
        self.assertEqual(
            'utf_16',
            test_codec_built_in_equivalent('utf_16_le_sig')
        )

    def test_uses_bom(self):
        self.assertTrue(uses_bom('utf_32'))
        self.assertFalse(uses_bom('utf_32_be'))
        self.assertTrue(uses_bom('utf_32_be_sig'))
        self.assertFalse(uses_bom('utf_32_le'))
        self.assertTrue(uses_bom('utf_32_le_sig'))

        self.assertTrue(uses_bom('utf_16'))
        self.assertFalse(uses_bom('utf_16_be'))
        self.assertTrue(uses_bom('utf_16_be_sig'))
        self.assertFalse(uses_bom('utf_16_le'))
        self.assertTrue(uses_bom('utf_16_le_sig'))

        self.assertFalse(uses_bom('utf_8'))
        self.assertTrue(uses_bom('utf_8_sig'))

    def test_encoding_detectable(self):
        # No BOM + nothing
        self.assertFalse(encoding_detectable('', 'utf_32_be'))
        self.assertFalse(encoding_detectable('', 'utf_32_le'))

        self.assertFalse(encoding_detectable('', 'utf_16_be'))
        self.assertFalse(encoding_detectable('', 'utf_16_le'))

        self.assertFalse(encoding_detectable('', 'utf_8'))
        # BOM + nothing
        self.assertTrue(encoding_detectable('', 'utf_32'))
        self.assertTrue(encoding_detectable('', 'utf_32_be_sig'))
        self.assertTrue(encoding_detectable('', 'utf_32_le_sig'))

        self.assertTrue(encoding_detectable('', 'utf_16'))
        self.assertTrue(encoding_detectable('', 'utf_16_be_sig'))
        self.assertTrue(encoding_detectable('', 'utf_16_le_sig'))

        self.assertTrue(encoding_detectable('', 'utf_8_sig'))
        # No BOM + non-ASCII
        self.assertFalse(encoding_detectable('Ⓝⓔ', 'utf_32_be'))
        self.assertFalse(encoding_detectable('ⓥⓔ', 'utf_32_le'))

        self.assertFalse(encoding_detectable('ⓡ ', 'utf_16_be'))
        self.assertFalse(encoding_detectable('ⓖⓞ', 'utf_16_le'))

        self.assertFalse(encoding_detectable('ⓝⓝ', 'utf_8'))
        # No BOM + ASCII
        self.assertTrue(encoding_detectable('a ', 'utf_32_be'))
        self.assertTrue(encoding_detectable('gi', 'utf_32_le'))

        self.assertTrue(encoding_detectable('ve', 'utf_16_be'))
        self.assertTrue(encoding_detectable(' y', 'utf_16_le'))

        self.assertTrue(encoding_detectable('ou', 'utf_8'))
        # BOM + non-ASCII
        self.assertTrue(encoding_detectable('␣ⓤ', 'utf_32'))
        self.assertTrue(encoding_detectable('ⓟ␤', 'utf_32_be_sig'))
        self.assertTrue(encoding_detectable('Ⓝⓔ', 'utf_32_le_sig'))

        self.assertTrue(encoding_detectable('ⓥⓔ', 'utf_16'))
        self.assertTrue(encoding_detectable('ⓡ␣', 'utf_16_be_sig'))
        self.assertTrue(encoding_detectable('ⓖⓞ', 'utf_16_le_sig'))

        self.assertTrue(encoding_detectable('ⓝⓝ', 'utf_8_sig'))
        # BOM + ASCII
        self.assertTrue(encoding_detectable('a ', 'utf_32'))
        self.assertTrue(encoding_detectable('le', 'utf_32_be_sig'))
        self.assertTrue(encoding_detectable('t ', 'utf_32_le_sig'))

        self.assertTrue(encoding_detectable('yo', 'utf_16'))
        self.assertTrue(encoding_detectable('u ', 'utf_16_be_sig'))
        self.assertTrue(encoding_detectable('do', 'utf_16_le_sig'))

        self.assertTrue(encoding_detectable('wn', 'utf_8_sig'))


class DecoderTestCase(unittest.TestCase):
    def test_detect_encoding(self):
        error1 = "{} was encoded with {}, but detect_encoding() returned {}."
        error2 = "detect_encoding({}) returned a codec that isn’t built-in."
        for string in test_strings:
            for codec in utf_codecs():
                input = string.encode(codec)

                if not uses_bom(codec) and len(string) == 0:
                    expected_output = 'utf_8'
                elif not encoding_detectable(string, codec):
                    expected_output = None
                elif is_test_codec(codec):
                    expected_output = test_codec_built_in_equivalent(codec)
                else:
                    expected_output = codec

                actual_output = decoder.detect_encoding(input)
                if expected_output is not None:
                    self.assertEqual(
                        expected_output,
                        actual_output,
                        msg=error1.format(
                            input,
                            repr(codec),
                            repr(actual_output)
                        )
                    )

                codec_info = codecs.lookup(actual_output)
                self.assertFalse(
                    is_test_codec(codec_info),
                    msg=error2.format(input)
                )

    def test_auto_decode(self):
        lenient_error_handlers = (
            'ignore',
            'replace',
            'backslashreplace',
            'surrogateescape',
        )
        at_least_one_decode_error = False
        for string in test_strings:
            for codec in utf_codecs():
                input = string.encode(codec)
                if encoding_detectable(string, codec) or len(string) == 0:
                    actual_output = decoder.auto_decode(input)
                    self.assertEqual(
                        string,
                        actual_output,
                        msg=f"auto_decode({input}) returned the wrong value."
                    )
                    self.assertIsInstance(actual_output, str)
                else:
                    try:
                        decoder.auto_decode(input)
                    except UnicodeDecodeError:
                        at_least_one_decode_error = True

                for handler in lenient_error_handlers:
                    actual_output = decoder.auto_decode(input, errors=handler)
                    self.assertIsInstance(actual_output, str)
        self.assertTrue(
            at_least_one_decode_error,
            msg="None of the test_strings triggered a decoding error."
        )

    def perform_lines_in_file_test(self, strings):
        workspace = ws_with_files_in_many_codecs('{}', '\n'.join(strings))
        with temp_workspace(workspace):
            iterable = zip(
                itertools.cycle(strings),
                decoder.lines_in_files(workspace.keys())
            )
            for item in iterable:
                self.assertEqual(item[0], item[1])

    def test_lines_in_file(self):
        self.perform_lines_in_file_test((
            "YAML",
            "ⓎⒶⓂⓁ",
            "🅨🅐🅜🅛",
            "ＹＡＭＬ"
        ))
        self.perform_lines_in_file_test((
            "𝐘𝐀𝐌𝐋",
            "𝖄𝕬𝕸𝕷",
            "𝒀𝑨𝑴𝑳",
            "𝓨𝓐𝓜𝓛"
        ))
