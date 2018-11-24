# -*- coding: utf-8 -*-
# Copyright (C) 2017 Adrien Vergé
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

import os
import shutil
import subprocess
import tempfile
import sys
import unittest


PYTHON = sys.executable or 'python'


class ModuleTestCase(unittest.TestCase):
    def setUp(self):
        self.wd = tempfile.mkdtemp(prefix='yamllint-tests-')

        # file with only one warning
        with open(os.path.join(self.wd, 'warn.yaml'), 'w') as f:
            f.write('key: value\n')

        # file in dir
        os.mkdir(os.path.join(self.wd, 'sub'))
        with open(os.path.join(self.wd, 'sub', 'nok.yaml'), 'w') as f:
            f.write('---\n'
                    'list: [  1, 1, 2, 3, 5, 8]  \n')

    def tearDown(self):
        shutil.rmtree(self.wd)

    def test_run_module_no_args(self):
        with self.assertRaises(subprocess.CalledProcessError) as ctx:
            subprocess.check_output([PYTHON, '-m', 'yamllint'],
                                    stderr=subprocess.STDOUT)
        self.assertEqual(ctx.exception.returncode, 2)
        self.assertRegexpMatches(ctx.exception.output.decode(),
                                 r'^usage: yamllint')

    def test_run_module_on_bad_dir(self):
        with self.assertRaises(subprocess.CalledProcessError) as ctx:
            subprocess.check_output([PYTHON, '-m', 'yamllint',
                                     '/does/not/exist'],
                                    stderr=subprocess.STDOUT)
        self.assertRegexpMatches(ctx.exception.output.decode(),
                                 r'No such file or directory')

    def test_run_module_on_file(self):
        out = subprocess.check_output(
            [PYTHON, '-m', 'yamllint', os.path.join(self.wd, 'warn.yaml')])
        lines = out.decode().splitlines()
        self.assertIn('/warn.yaml', lines[0])
        self.assertEqual('\n'.join(lines[1:]),
                         '  1:1       warning  missing document start "---"'
                         '  (document-start)\n')

    def test_run_module_on_dir(self):
        with self.assertRaises(subprocess.CalledProcessError) as ctx:
            subprocess.check_output([PYTHON, '-m', 'yamllint', self.wd])
        self.assertEqual(ctx.exception.returncode, 1)

        files = ctx.exception.output.decode().split('\n\n')
        self.assertIn(
            '/warn.yaml\n'
            '  1:1       warning  missing document start "---"'
            '  (document-start)',
            files[0])
        self.assertIn(
            '/sub/nok.yaml\n'
            '  2:9       error    too many spaces inside brackets'
            '  (brackets)\n'
            '  2:27      error    trailing spaces  (trailing-spaces)',
            files[1])
