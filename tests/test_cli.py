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

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import os
import shutil
import tempfile
import unittest
import sys

from yamllint import cli


class CommandLineTestCase(unittest.TestCase):
    def setUp(self):
        self.wd = tempfile.mkdtemp(prefix='yamllint-tests-')

        # .yaml file at root
        with open(os.path.join(self.wd, 'a.yaml'), 'w') as f:
            f.write('---\n'
                    '- 1   \n'
                    '- 2')

        # .yml file at root
        open(os.path.join(self.wd, 'empty.yml'), 'w').close()

        # file in dir
        os.mkdir(os.path.join(self.wd, 'sub'))
        with open(os.path.join(self.wd, 'sub', 'ok.yaml'), 'w') as f:
            f.write('---\n'
                    'key: value\n')

        # file in very nested dir
        dir = self.wd
        for i in range(15):
            dir = os.path.join(dir, 's')
            os.mkdir(dir)
        with open(os.path.join(dir, 'file.yaml'), 'w') as f:
            f.write('---\n'
                    'key: value\n'
                    'key: other value\n')

        # empty dir
        os.mkdir(os.path.join(self.wd, 'empty-dir'))

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
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/ok.yaml')],
        )

        items = [os.path.join(self.wd, 'sub/ok.yaml'),
                 os.path.join(self.wd, 'empty-dir')]
        self.assertEqual(
            sorted(cli.find_files_recursively(items)),
            [os.path.join(self.wd, 'sub/ok.yaml')],
        )

        items = [os.path.join(self.wd, 'empty.yml'),
                 os.path.join(self.wd, 's')]
        self.assertEqual(
            sorted(cli.find_files_recursively(items)),
            [os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml')],
        )

        items = [os.path.join(self.wd, 'sub'),
                 os.path.join(self.wd, '/etc/another/file')]
        self.assertEqual(
            sorted(cli.find_files_recursively(items)),
            [os.path.join(self.wd, '/etc/another/file'),
             os.path.join(self.wd, 'sub/ok.yaml')],
        )

    def test_run_with_bad_arguments(self):
        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(())

        self.assertNotEqual(ctx.exception.code, 0)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, '')
        self.assertRegexpMatches(err, r'^usage')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('--unknown-arg', ))

        self.assertNotEqual(ctx.exception.code, 0)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, '')
        self.assertRegexpMatches(err, r'^usage')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-c', './conf.yaml', '-d', 'relaxed', 'file'))

        self.assertNotEqual(ctx.exception.code, 0)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, '')
        self.assertRegexpMatches(err, r'^Options --config-file and '
                                      r'--config-data cannot be used')

    def test_run_with_bad_config(self):
        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-d', 'rules: {a: b}', 'file'))

        self.assertEqual(ctx.exception.code, -1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, '')
        self.assertRegexpMatches(err, r'^invalid config: no such rule')

    def test_run_with_empty_config(self):
        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-d', '', 'file'))

        self.assertEqual(ctx.exception.code, -1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, '')
        self.assertRegexpMatches(err, r'^invalid config: not a dict')

    def test_run_with_config_file(self):
        with open(os.path.join(self.wd, 'config'), 'w') as f:
            f.write('rules: {trailing-spaces: disable}')

        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-c', f.name, os.path.join(self.wd, 'a.yaml')))
        self.assertEqual(ctx.exception.code, 0)

        with open(os.path.join(self.wd, 'config'), 'w') as f:
            f.write('rules: {trailing-spaces: enable}')

        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-c', f.name, os.path.join(self.wd, 'a.yaml')))
        self.assertEqual(ctx.exception.code, 1)

    def test_run_with_user_global_config_file(self):
        home = os.path.join(self.wd, 'fake-home')
        os.mkdir(home)
        dir = os.path.join(home, '.config')
        os.mkdir(dir)
        dir = os.path.join(dir, 'yamllint')
        os.mkdir(dir)
        config = os.path.join(dir, 'config')

        temp = os.environ['HOME']
        os.environ['HOME'] = home

        with open(config, 'w') as f:
            f.write('rules: {trailing-spaces: disable}')

        with self.assertRaises(SystemExit) as ctx:
            cli.run((os.path.join(self.wd, 'a.yaml'), ))
        self.assertEqual(ctx.exception.code, 0)

        with open(config, 'w') as f:
            f.write('rules: {trailing-spaces: enable}')

        with self.assertRaises(SystemExit) as ctx:
            cli.run((os.path.join(self.wd, 'a.yaml'), ))
        self.assertEqual(ctx.exception.code, 1)

        os.environ['HOME'] = temp

    def test_run_version(self):
        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('--version', ))

        self.assertEqual(ctx.exception.code, 0)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertRegexpMatches(out + err, r'yamllint \d+\.\d+')

    def test_run_non_existing_file(self):
        file = os.path.join(self.wd, 'i-do-not-exist.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-f', 'parsable', file))

        self.assertEqual(ctx.exception.code, -1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, '')
        self.assertRegexpMatches(err, r'No such file or directory')

    def test_run_one_problem_file(self):
        file = os.path.join(self.wd, 'a.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-f', 'parsable', file))

        self.assertEqual(ctx.exception.code, 1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, (
            '%s:2:4: [error] trailing spaces (trailing-spaces)\n'
            '%s:3:4: [error] no new line character at the end of file '
            '(new-line-at-end-of-file)\n') % (file, file))
        self.assertEqual(err, '')

    def test_run_one_ok_file(self):
        file = os.path.join(self.wd, 'sub', 'ok.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-f', 'parsable', file))

        self.assertEqual(ctx.exception.code, 0)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, '')
        self.assertEqual(err, '')

    def test_run_empty_file(self):
        file = os.path.join(self.wd, 'empty.yml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-f', 'parsable', file))

        self.assertEqual(ctx.exception.code, 0)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, '')
        self.assertEqual(err, '')

    def test_run_multiple_files(self):
        items = [os.path.join(self.wd, 'empty.yml'),
                 os.path.join(self.wd, 's')]
        file = items[1] + '/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(['-f', 'parsable'] + items)

        self.assertEqual(ctx.exception.code, 1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, (
            '%s:3:1: [error] duplication of key "key" in mapping '
            '(key-duplicates)\n') % file)
        self.assertEqual(err, '')

    def test_run_colored_output(self):
        file = os.path.join(self.wd, 'a.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run((file, ))

        self.assertEqual(ctx.exception.code, 1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, (
            '\033[4m%s\033[0m\n'
            '  \033[2m2:4\033[0m       \033[31merror\033[0m    '
            'trailing spaces  \033[2m(trailing-spaces)\033[0m\n'
            '  \033[2m3:4\033[0m       \033[31merror\033[0m    '
            'no new line character at the end of file  '
            '\033[2m(new-line-at-end-of-file)\033[0m\n'
            '\n' % file))
        self.assertEqual(err, '')
