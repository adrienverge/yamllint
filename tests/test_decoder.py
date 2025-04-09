# Copyright (C) 2023–2025 Jason Yundt
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
import os
import unittest

from tests.common import (
    UTF_CODECS,
    built_in_equivalent_of_test_codec,
    encoding_detectable,
    is_test_codec,
    register_test_codecs,
    temp_workspace,
    temp_workspace_with_files_in_many_codecs,
    unregister_test_codecs,
    uses_bom,
)

from yamllint import decoder


class PreEncodedTestStringInfo:
    def __init__(
        self,
        input_bytes,
        codec_for_input_bytes,
        expected_output_str
    ):
        self.input_bytes = input_bytes
        self.codec_for_input_bytes = codec_for_input_bytes
        self.expected_output_str = expected_output_str


PRE_ENCODED_TEST_STRING_INFOS = (
    # An empty string
    PreEncodedTestStringInfo(
        b'',
        None,
        ''
    ),

    # A single ASCII character
    PreEncodedTestStringInfo(
        b'\x00\x00\x00|',
        'utf_32_be',
        '|'
    ),
    PreEncodedTestStringInfo(
        b'\x00\x00\xfe\xff\x00\x00\x00|',
        'utf_32',
        '|'
    ),
    PreEncodedTestStringInfo(
        b'|\x00\x00\x00',
        'utf_32_le',
        '|'
    ),
    PreEncodedTestStringInfo(
        b'\xff\xfe\x00\x00|\x00\x00\x00',
        'utf_32',  # LE with BOM
        '|'
    ),
    PreEncodedTestStringInfo(
        b'\x00|',
        'utf_16_be',
        '|'
    ),
    PreEncodedTestStringInfo(
        b'\xfe\xff\x00|',
        'utf_16',  # BE with BOM
        '|'
    ),
    PreEncodedTestStringInfo(
        b'|\x00',
        'utf_16_le',
        '|'
    ),
    PreEncodedTestStringInfo(
        b'\xff\xfe|\x00',
        'utf_16',   # LE with BOM
        '|'
    ),
    PreEncodedTestStringInfo(
        b'|',
        'utf_8',
        '|'
    ),
    PreEncodedTestStringInfo(
        b'\xef\xbb\xbf|',
        'utf_8_sig',
        '|'
    ),

    # A string that starts with an ASCII character
    PreEncodedTestStringInfo(
        b'\x00\x00\x00W\x00\x00\x00h\x00\x00\x00a\x00\x00\x00t\x00\x00 \x19\x00\x00\x00s\x00\x00\x00 \x00\x00\x00u\x00\x00\x00p\x00\x00\x00?',  # noqa: E501
        'utf_32_be',
        'What’s up?'
    ),
    PreEncodedTestStringInfo(
        b'\x00\x00\xfe\xff\x00\x00\x00W\x00\x00\x00h\x00\x00\x00a\x00\x00\x00t\x00\x00 \x19\x00\x00\x00s\x00\x00\x00 \x00\x00\x00u\x00\x00\x00p\x00\x00\x00?',  # noqa: E501
        'utf_32',  # BE with BOM
        'What’s up?'
    ),
    PreEncodedTestStringInfo(
        b'W\x00\x00\x00h\x00\x00\x00a\x00\x00\x00t\x00\x00\x00\x19 \x00\x00s\x00\x00\x00 \x00\x00\x00u\x00\x00\x00p\x00\x00\x00?\x00\x00\x00',  # noqa: E501
        'utf_32_le',
        'What’s up?'
    ),
    PreEncodedTestStringInfo(
        b'\xff\xfe\x00\x00W\x00\x00\x00h\x00\x00\x00a\x00\x00\x00t\x00\x00\x00\x19 \x00\x00s\x00\x00\x00 \x00\x00\x00u\x00\x00\x00p\x00\x00\x00?\x00\x00\x00',  # noqa: E501
        'utf_32',  # LE with BOM
        'What’s up?'
    ),
    PreEncodedTestStringInfo(
        b'\x00W\x00h\x00a\x00t \x19\x00s\x00 \x00u\x00p\x00?',
        'utf_16_be',
        'What’s up?'
    ),
    PreEncodedTestStringInfo(
        b'\xfe\xff\x00W\x00h\x00a\x00t \x19\x00s\x00 \x00u\x00p\x00?',
        'utf_16',  # BE with BOM
        'What’s up?'
    ),
    PreEncodedTestStringInfo(
        b'W\x00h\x00a\x00t\x00\x19 s\x00 \x00u\x00p\x00?\x00',
        'utf_16_le',
        'What’s up?'
    ),
    PreEncodedTestStringInfo(
        b'\xff\xfeW\x00h\x00a\x00t\x00\x19 s\x00 \x00u\x00p\x00?\x00',
        'utf_16',  # LE with BOM
        'What’s up?'
    ),
    PreEncodedTestStringInfo(
        b'What\xe2\x80\x99s up?',
        'utf_8',
        'What’s up?'
    ),
    PreEncodedTestStringInfo(
        b'\xef\xbb\xbfWhat\xe2\x80\x99s up?',
        'utf_8_sig',
        'What’s up?'
    ),

    # A single non-ASCII character
    PreEncodedTestStringInfo(
        b'\x00\x00\xfe\xff\x00\x01\xf4;',
        'utf_32',  # BE with BOM
        '🐻'
    ),
    PreEncodedTestStringInfo(
        b'\xff\xfe\x00\x00;\xf4\x01\x00',
        'utf_32',  # LE with BOM
        '🐻'
    ),
    PreEncodedTestStringInfo(
        b'\xfe\xff\xd8=\xdc;',
        'utf_16',  # BE with BOM
        '🐻'
    ),
    PreEncodedTestStringInfo(
        b'\xff\xfe=\xd8;\xdc',
        'utf_16',  # LE with BOM
        '🐻'
    ),
    PreEncodedTestStringInfo(
        b'\xef\xbb\xbf\xf0\x9f\x90\xbb',
        'utf_8_sig',
        '🐻'
    ),

    # A string that starts with a non-ASCII character
    PreEncodedTestStringInfo(
        b'\x00\x00\xfe\xff\x00\x00\x00\xc7\x00\x00\x00a\x00\x00\x00 \x00\x00\x00v\x00\x00\x00a\x00\x00\x00?',  # noqa: E501
        'utf_32',  # BE with BOM
        'Ça va?'
    ),
    PreEncodedTestStringInfo(
        b'\xff\xfe\x00\x00\xc7\x00\x00\x00a\x00\x00\x00 \x00\x00\x00v\x00\x00\x00a\x00\x00\x00?\x00\x00\x00',  # noqa: E501
        'utf_32',  # LE with BOM
        'Ça va?'
    ),
    PreEncodedTestStringInfo(
        b'\xfe\xff\x00\xc7\x00a\x00 \x00v\x00a\x00?',
        'utf_16',  # BE with BOM
        'Ça va?'
    ),
    PreEncodedTestStringInfo(
        b'\xff\xfe\xc7\x00a\x00 \x00v\x00a\x00?\x00',
        'utf_16',  # LE with BOM
        'Ça va?'
    ),
    PreEncodedTestStringInfo(
        b'\xef\xbb\xbf\xc3\x87a va?',
        'utf_8_sig',
        'Ça va?'
    )
)
TEST_STRINGS_TO_ENCODE_AT_RUNTIME = (
    "",
    "y",
    "yaml",
    "🇾⁠🇦⁠🇲⁠🇱⁠❗"
)


def setUpModule():
    register_test_codecs()
    try:
        del os.environ['YAMLLINT_FILE_ENCODING']
    except KeyError:
        pass


tearDownModule = unregister_test_codecs


class EncodingStuffFromCommonTestCase(unittest.TestCase):
    def test_test_codecs_and_utf_codecs(self):
        error = "{} failed to correctly encode then decode {}."
        for string in TEST_STRINGS_TO_ENCODE_AT_RUNTIME:
            for codec in UTF_CODECS:
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

    def test_built_in_equivalent_of_test_codec(self):
        self.assertEqual(
            'utf_32',
            built_in_equivalent_of_test_codec('utf_32_be_sig')
        )
        self.assertEqual(
            'utf_32',
            built_in_equivalent_of_test_codec('utf_32_le_sig')
        )

        self.assertEqual(
            'utf_16',
            built_in_equivalent_of_test_codec('utf_16_be_sig')
        )
        self.assertEqual(
            'utf_16',
            built_in_equivalent_of_test_codec('utf_16_le_sig')
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
    def detect_encoding_test_helper(self, input_bytes, expected_codec):
        ERROR1 = "{} was encoded with {}, but detect_encoding() returned {}."
        ERROR2 = "detect_encoding({}) returned a codec that isn’t built-in."
        actual_codec = decoder.detect_encoding(input_bytes)
        if expected_codec is not None:
            self.assertEqual(
                expected_codec,
                actual_codec,
                msg=ERROR1.format(
                    input_bytes,
                    repr(expected_codec),
                    repr(actual_codec)
                )
            )

        codec_info = codecs.lookup(actual_codec)
        self.assertFalse(
            is_test_codec(codec_info),
            msg=ERROR2.format(input_bytes)
        )

    def test_detect_encoding_with_pre_encoded_strings(self):
        for pre_encoded_test_string_info in PRE_ENCODED_TEST_STRING_INFOS:
            self.detect_encoding_test_helper(
                pre_encoded_test_string_info.input_bytes,
                pre_encoded_test_string_info.codec_for_input_bytes
            )

    def test_detect_encoding_with_strings_encoded_at_runtime(self):
        for string in TEST_STRINGS_TO_ENCODE_AT_RUNTIME:
            for codec in UTF_CODECS:
                if not uses_bom(codec) and len(string) == 0:
                    expected_codec = 'utf_8'
                elif not encoding_detectable(string, codec):
                    expected_codec = None
                elif is_test_codec(codec):
                    expected_codec = built_in_equivalent_of_test_codec(codec)
                else:
                    expected_codec = codec
                self.detect_encoding_test_helper(
                    string.encode(codec),
                    expected_codec
                )

    def test_detect_encoding_with_env_var_override(self):
        # These three encodings were chosen randomly.
        NONSTANDARD_ENCODINGS = ('iso8859_6', 'iso8859_11', 'euc_jis_2004')
        RANDOM_BYTES = b'\x90Jg\xd9rS\x95\xd6[\x1d\x8b\xc4Ir\x0fC'
        for nonstandard_encoding in NONSTANDARD_ENCODINGS:
            os.environ['YAMLLINT_FILE_ENCODING'] = nonstandard_encoding
            self.assertEqual(
                decoder.detect_encoding(RANDOM_BYTES),
                nonstandard_encoding
            )
        del os.environ['YAMLLINT_FILE_ENCODING']

    def auto_decode_test_helper(
        self,
        input_bytes,
        codec_for_input_bytes,
        expected_string
    ):
        ERROR = "auto_decode({}) returned the wrong value."
        does_auto_detect_encodings_return_value_matter = (
            codec_for_input_bytes is not None and (
                encoding_detectable(expected_string, codec_for_input_bytes)
                or len(input_bytes) == 0
            )
        )
        if does_auto_detect_encodings_return_value_matter:
            actual_output = decoder.auto_decode(input_bytes)
            self.assertEqual(
                expected_string,
                actual_output,
                msg=ERROR.format(repr(input_bytes))
            )
            self.assertIsInstance(actual_output, str)
        else:
            decoder.auto_decode(input_bytes)

    def test_auto_decode_with_pre_encoded_strings(self):
        for pre_encoded_test_string_info in PRE_ENCODED_TEST_STRING_INFOS:
            self.auto_decode_test_helper(
                pre_encoded_test_string_info.input_bytes,
                pre_encoded_test_string_info.codec_for_input_bytes,
                pre_encoded_test_string_info.expected_output_str
            )

    def test_auto_decode_with_strings_encoded_at_runtime(self):
        at_least_one_decode_error = False
        for string in TEST_STRINGS_TO_ENCODE_AT_RUNTIME:
            for codec in UTF_CODECS:
                try:
                    self.auto_decode_test_helper(
                        string.encode(codec),
                        codec,
                        string
                    )
                except UnicodeDecodeError:
                    at_least_one_decode_error = True
        self.assertTrue(
            at_least_one_decode_error,
            msg=("None of the TEST_STRINGS_TO_ENCODE_AT_RUNTIME triggered a "
                 "decoding error.")
        )

    def perform_lines_in_file_test(self, strings):
        workspace = temp_workspace_with_files_in_many_codecs(
            '{}',
            '\n'.join(strings)
        )
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
