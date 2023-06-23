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

GREEK = """---
greek:
  8: [Θ, θ, θήτα, [тета], Т]
  20: [Υ, υ, ύψιλον, [ипсилон], И]
"""

CP1252 = """---
capitals:
  1: Reykjavík
  2: Tórshavn
"""

ENC = ['utf-8']


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
        cls.create_file(CP1252, 'cp1252', False)

    @classmethod
    def tearDownClass(cls):
        super(UnicodeTestCase, cls).tearDownClass()

        shutil.rmtree(cls.wd)
        locale.setlocale(locale.LC_ALL, cls.slc)

    def run_fobj(self, fobj):
        decnt = 0
        pcnt = 0
        for p in linter.run(fobj, self.cfg):
            if p.rule == 'document-end' or p.line == 4:
                decnt += 1
            else:
                print('UnicodeTestCase', p.desc, p.line, p.rule)
                pcnt += 1
        self.assertEqual(decnt, 1)
        self.assertEqual(pcnt, 0)

    def run_file(self, lc, enc, bom):
        try:
            locale.setlocale(locale.LC_ALL, lc)
            with open(self.fn(enc, bom)) as f:
                self.run_fobj(f)
            locale.setlocale(locale.LC_ALL, self.slc)
        except locale.Error:
            self.skipTest('locale ' + lc + ' not available')

    def run_bytes(self, body, enc, bom, buf):
        bs = (("\uFEFF" if bom else "") + body).encode(enc)
        if buf:
            self.run_fobj(io.TextIOWrapper(io.BufferedReader(io.BytesIO(bs))))
        else:
            self.run_fobj(io.TextIOWrapper(io.BytesIO(bs)))

    def test_file_en_US_UTF_8_utf8_nob(self):
        self.run_file('en_US.UTF-8', 'utf-8', False)

    def test_file_ru_RU_CP1251_utf8_nob(self):
        self.run_file('ru_RU.CP1251', 'utf-8', False)

    @unittest.expectedFailure
    def test_file_en_US_utf8_cp1252(self):
        self.run_file('en_US.utf8' if sys.platform.startswith('linux')
                      else 'en_US.UTF-8',
                      'cp1252', False)

    @unittest.expectedFailure
    def test_file_en_US_ISO8859_1_cp1252(self):
        self.run_file('en_US.ISO8859-1', 'cp1252', False)

    def test_file_C_utf8_nob(self):
        self.run_file('C', 'utf-8', False)

    def test_file_C_utf8(self):
        self.run_file('C', 'utf-8', True)

    def test_bytes_utf8_nob(self):
        self.run_bytes(GREEK, 'utf-8', False, False)
