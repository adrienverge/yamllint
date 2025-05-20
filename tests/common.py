# Copyright (C) 2016 Adrien Vergé
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
import contextlib
from io import StringIO
import os
import shutil
import sys
import tempfile
import unittest
import warnings
from codecs import CodecInfo

import yaml

from yamllint import linter
from yamllint.config import YamlLintConfig


# Encoding related stuff:
UTF_CODECS = (
    'utf_32_be',
    'utf_32_be_sig',
    'utf_32_le',
    'utf_32_le_sig',
    'utf_16_be',
    'utf_16_be_sig',
    'utf_16_le',
    'utf_16_le_sig',
    'utf_8',
    'utf_8_sig'
)


def encode_utf_32_be_sig(obj):
    return (
        codecs.BOM_UTF32_BE + codecs.encode(obj, 'utf_32_be', 'strict'),
        len(obj)
    )


def encode_utf_32_le_sig(obj):
    return (
        codecs.BOM_UTF32_LE + codecs.encode(obj, 'utf_32_le', 'strict'),
        len(obj)
    )


def encode_utf_16_be_sig(obj):
    return (
        codecs.BOM_UTF16_BE + codecs.encode(obj, 'utf_16_be', 'strict'),
        len(obj)
    )


def encode_utf_16_le_sig(obj):
    return (
        codecs.BOM_UTF16_LE + codecs.encode(obj, 'utf_16_le', 'strict'),
        len(obj)
    )


test_codec_infos = {
    'utf_32_be_sig':
    CodecInfo(encode_utf_32_be_sig, codecs.getdecoder('utf_32')),
    'utf_32_le_sig':
    CodecInfo(encode_utf_32_le_sig, codecs.getdecoder('utf_32')),
    'utf_16_be_sig':
    CodecInfo(encode_utf_16_be_sig, codecs.getdecoder('utf_16')),
    'utf_16_le_sig':
    CodecInfo(encode_utf_16_le_sig, codecs.getdecoder('utf_16')),
}


def register_test_codecs():
    codecs.register(test_codec_infos.get)


def unregister_test_codecs():
    if sys.version_info >= (3, 10, 0):
        codecs.unregister(test_codec_infos.get)
    else:
        warnings.warn(
            "This version of Python doesn’t allow us to unregister codecs.",
            stacklevel=1
        )


def is_test_codec(codec):
    return codec in test_codec_infos.keys()


def built_in_equivalent_of_test_codec(test_codec):
    return_value = test_codec
    for suffix in ('_sig', '_be', '_le'):
        return_value = return_value.replace(suffix, '')
    return return_value


def uses_bom(codec):
    for suffix in ('_32', '_16', '_sig'):
        if codec.endswith(suffix):
            return True
    return False


def encoding_detectable(string, codec):
    """
    Returns True if encoding can be detected after string is encoded

    Encoding detection only works if you’re using a BOM or the first character
    is ASCII. See yamllint.decoder.auto_decode()’s docstring.
    """
    return uses_bom(codec) or (len(string) > 0 and string[0].isascii())


# Workspace related stuff:
class Blob:
    def __init__(self, text, encoding):
        self.text = text
        self.encoding = encoding


def build_temp_workspace(files):
    tempdir = tempfile.mkdtemp(prefix='yamllint-tests-')

    for path, content in files.items():
        path = os.fsencode(os.path.join(tempdir, path))
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        if isinstance(content, list):
            os.mkdir(path)
        elif isinstance(content, str) and content.startswith('symlink://'):
            os.symlink(content[10:], path)
        else:
            if isinstance(content, Blob):
                content = content.text.encode(content.encoding)
            elif isinstance(content, str):
                content = content.encode('utf_8')
            with open(path, 'wb') as f:
                f.write(content)

    return tempdir


@contextlib.contextmanager
def temp_workspace(files):
    """Provide a temporary workspace that is automatically cleaned up."""
    backup_wd = os.getcwd()
    wd = build_temp_workspace(files)

    try:
        os.chdir(wd)
        yield
    finally:
        os.chdir(backup_wd)
        shutil.rmtree(wd)


def temp_workspace_with_files_in_many_codecs(path_template, text):
    workspace = {}
    for codec in UTF_CODECS:
        if encoding_detectable(text, codec):
            workspace[path_template.format(codec)] = Blob(text, codec)
    return workspace


# Miscellaneous stuff:
class RuleTestCase(unittest.TestCase):
    def build_fake_config(self, conf):
        if conf is None:
            conf = {}
        else:
            conf = yaml.safe_load(conf)
        conf = {'extends': 'default',
                'rules': conf}
        return YamlLintConfig(yaml.safe_dump(conf))

    def check(self, source, conf, **kwargs):
        expected_problems = []
        for key in kwargs:
            assert key.startswith('problem')
            if len(kwargs[key]) > 2:
                if kwargs[key][2] == 'syntax':
                    rule_id = None
                else:
                    rule_id = kwargs[key][2]
            else:
                rule_id = self.rule_id
            expected_problems.append(linter.LintProblem(
                kwargs[key][0], kwargs[key][1], rule=rule_id))
        expected_problems.sort()

        real_problems = list(linter.run(source, self.build_fake_config(conf)))
        self.assertEqual(real_problems, expected_problems)


class RunContext:
    """Context manager for ``cli.run()`` to capture exit code and streams."""

    def __init__(self, case):
        self.stdout = self.stderr = None
        self._raises_ctx = case.assertRaises(SystemExit)

    def __enter__(self):
        self._raises_ctx.__enter__()
        self.old_sys_stdout = sys.stdout
        self.old_sys_stderr = sys.stderr
        sys.stdout = self.outstream = StringIO()
        sys.stderr = self.errstream = StringIO()
        return self

    def __exit__(self, *exc_info):
        self.stdout = self.outstream.getvalue()
        self.stderr = self.errstream.getvalue()
        sys.stdout = self.old_sys_stdout
        sys.stderr = self.old_sys_stderr
        return self._raises_ctx.__exit__(*exc_info)

    @property
    def returncode(self):
        return self._raises_ctx.exception.code
