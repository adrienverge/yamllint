# vim:set sw=4 ts=8 et fileencoding=utf8:
# Copyright (C) 2023 Serguei E. Leontiev
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

import io
import locale
import os
import shutil
import sys
import unittest

from tests.common import build_temp_workspace

from yamllint import linter
from yamllint.config import YamlLintConfig

CONFIG = """
extends: default
"""

GREEK = """---
greek:
  8: [Θ, θ, θήτα, [тета], Т]
  20: [Υ, υ, ύψιλον, [ипсилон], И]
"""
GREEK_P = set([('document-end', 4)])

CP1252 = """---
capitals:
  1: Reykjavík
  2: Tórshavn
"""
CP1252_P = set([('unicode-decode', 0)])

MINIMAL = "m:\n"
MINIMAL_P = set([('document-start', 1),
                 ('document-end', 1)])

FIRST = """Θ:\n"""
FIRST_P = set([('unicode-first-not-ascii', 1),
               ('document-start', 1),
               ('document-end', 1)])

ENC = ['utf-8', 'utf-16le', 'utf-16be', 'utf-32le', 'utf-32be']


class UnicodeTestCase(unittest.TestCase):
    @classmethod
    def fn(cls, enc: str, bom: bool) -> str:
        return os.path.join(cls.wd, enc + ("-bom" if bom else "") + ".yml")

    @classmethod
    def create_file(cls, body: str, enc: str, bom: bool) -> None:
        with open(cls.fn(enc, bom), 'w', encoding=enc) as f:
            f.write(("\uFEFF" if bom else "") + body)

    @classmethod
    def setUpClass(cls):
        super(UnicodeTestCase, cls).setUpClass()

        cls.slc = locale.getlocale(locale.LC_ALL)
        cls.cfg = YamlLintConfig('extends: default\n'
                                 'rules: {document-end: {level: warning}}\n'
                                 )
        cls.wd = build_temp_workspace({})
        for enc in ENC:
            cls.create_file(GREEK, enc, True)
            cls.create_file(GREEK, enc, False)
        cls.create_file(GREEK, 'utf-7', True)
        cls.create_file(CP1252, 'cp1252', False)
        cls.create_file(MINIMAL, 'ascii', False)

    @classmethod
    def tearDownClass(cls):
        super(UnicodeTestCase, cls).tearDownClass()

        shutil.rmtree(cls.wd)
        locale.setlocale(locale.LC_ALL, cls.slc)

    def run_fobj(self, fobj, exp):
        ep = exp.copy()
        pcnt = 0
        for p in linter.run(fobj, self.cfg):
            if (p.rule, p.line) in ep:
                ep.remove((p.rule, p.line),)
            else:
                print('UnicodeTestCase', p.desc, p.line, p.rule)
                pcnt += 1
        self.assertEqual(len(ep), 0)
        self.assertEqual(pcnt, 0)

    def run_file(self, lc, enc, bom, exp):
        try:
            locale.setlocale(locale.LC_ALL, lc)
            with open(self.fn(enc, bom)) as f:
                self.run_fobj(f, exp)
            locale.setlocale(locale.LC_ALL, self.slc)
        except locale.Error:
            self.skipTest('locale ' + lc + ' not available')

    def run_bytes(self, body, enc, bom, buf, exp):
        bs = (("\uFEFF" if bom else "") + body).encode(enc)
        if buf:
            self.run_fobj(io.TextIOWrapper(io.BufferedReader(io.BytesIO(bs))),
                          exp)
        else:
            self.run_fobj(io.TextIOWrapper(io.BytesIO(bs)), exp)

    def test_file_en_US_UTF_8_utf8_nob(self):
        self.run_file('en_US.UTF-8', 'utf-8', False, GREEK_P)

    def test_file_ru_RU_CP1251_utf8_nob(self):
        self.run_file('ru_RU.CP1251', 'utf-8', False, GREEK_P)

    def test_file_en_US_utf8_cp1252(self):
        self.run_file('en_US.utf8' if sys.platform.startswith('linux')
                      else 'en_US.UTF-8',
                      'cp1252', False, CP1252_P)

    def test_file_en_US_ISO8859_1_cp1252(self):
        self.run_file('en_US.ISO8859-1', 'cp1252', False, CP1252_P)

    def test_file_C_utf8_nob(self):
        self.run_file('C', 'utf-8', False, GREEK_P)

    def test_file_C_utf8(self):
        self.run_file('C', 'utf-8', True, GREEK_P)

    def test_file_C_utf16le_nob(self):
        self.run_file('C', 'utf-16le', False, GREEK_P)

    def test_file_C_utf16le(self):
        self.run_file('C', 'utf-16le', True, GREEK_P)

    def test_file_C_utf16be_nob(self):
        self.run_file('C', 'utf-16be', False, GREEK_P)

    def test_file_C_utf16be(self):
        self.run_file('C', 'utf-16be', True, GREEK_P)

    def test_file_C_utf32le_nob(self):
        self.run_file('C', 'utf-32le', False, GREEK_P)

    def test_file_C_utf32le(self):
        self.run_file('C', 'utf-32le', True, GREEK_P)

    def test_file_C_utf32be_nob(self):
        self.run_file('C', 'utf-32be', False, GREEK_P)

    def test_file_C_utf32be(self):
        self.run_file('C', 'utf-32be', True, GREEK_P)

    def test_file_C_utf7(self):
        self.run_file('C', 'utf-7', True, GREEK_P)

    def test_file_minimal_nob(self):
        self.run_file('C', 'ascii', False, MINIMAL_P)

    def test_bytes_utf8_nob(self):
        self.run_bytes(GREEK, 'utf-8', False, False, GREEK_P)

    def test_bytes_utf16(self):
        # .encode('utf-16') insert BOM automatically
        self.run_bytes(GREEK, 'utf-16', False, False, GREEK_P)

    def test_bytes_utf32_buf(self):
        # .encode('utf-32') insert BOM automatically
        self.run_bytes(GREEK, 'utf-32', False, True, GREEK_P)

    def test_bytes_minimal_nob(self):
        self.run_bytes(MINIMAL, 'ascii', False, False, MINIMAL_P)

    def test_bytes_minimal_nob_buf(self):
        self.run_bytes(MINIMAL, 'ascii', False, True, MINIMAL_P)

    def test_bytes_first_nob(self):
        self.run_bytes(FIRST, 'utf-8', False, False, FIRST_P)

    def test_bytes_first_nob_buf(self):
        self.run_bytes(FIRST, 'utf-8', False, True, FIRST_P)
