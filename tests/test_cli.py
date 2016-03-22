# -*- coding: utf-8 -*-
# Copyright (C) 2016 Adrien Vergé
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
import tempfile
import unittest

from yamllint import cli


class CommandLineTestCase(unittest.TestCase):
    def setUp(self):
        self.wd = tempfile.mkdtemp(prefix='yamllint-tests-')

        # .yaml file at root
        open(os.path.join(self.wd, 'a.yaml'), 'w').close()

        # .yml file at root
        open(os.path.join(self.wd, 'b.yml'), 'w').close()

        # file in dir
        os.mkdir(os.path.join(self.wd, 'sub'))
        with open(os.path.join(self.wd, 'sub', 'file.yaml'), 'w') as f:
            f.write('---\n'
                    'key: value\n')

        # file in very nested dir
        dir = self.wd
        for i in range(15):
            dir = os.path.join(dir, 's')
            os.mkdir(dir)
        with open(os.path.join(dir, 'file.yaml'), 'w') as f:
            f.write('---\n'
                    'key: value\n')

        # empty dir
        os.mkdir(os.path.join(self.wd, 'empty'))

        # non-YAML file
        with open(os.path.join(self.wd, 'no-yaml.json'), 'w') as f:
            f.write('---\n'
                    'key: value\n')

    def tearDown(self):
        shutil.rmtree(self.wd)

    def test_find_files_recursively(self):
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd])),
            [os.path.join(self.wd, 'a.yaml'),
             os.path.join(self.wd, 'b.yml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/file.yaml')],
        )

        items = [os.path.join(self.wd, 'sub/file.yaml'),
                 os.path.join(self.wd, 'empty')]
        self.assertEqual(
            sorted(cli.find_files_recursively(items)),
            [os.path.join(self.wd, 'sub/file.yaml')],
        )

        items = [os.path.join(self.wd, 'b.yml'),
                 os.path.join(self.wd, 's')]
        self.assertEqual(
            sorted(cli.find_files_recursively(items)),
            [os.path.join(self.wd, 'b.yml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml')],
        )

        items = [os.path.join(self.wd, 'sub'),
                 os.path.join(self.wd, '/etc/another/file')]
        self.assertEqual(
            sorted(cli.find_files_recursively(items)),
            [os.path.join(self.wd, '/etc/another/file'),
             os.path.join(self.wd, 'sub/file.yaml')],
        )
