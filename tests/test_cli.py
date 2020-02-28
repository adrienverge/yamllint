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
import fcntl
import locale
import os
import pty
import shutil
import sys
import unittest

from tests.common import build_temp_workspace

from yamllint import cli
from yamllint import config


class CommandLineTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(CommandLineTestCase, cls).setUpClass()

        cls.wd = build_temp_workspace({
            # .yaml file at root
            'a.yaml': '---\n'
                      '- 1   \n'
                      '- 2',
            # file with only one warning
            'warn.yaml': 'key: value\n',
            # .yml file at root
            'empty.yml': '',
            # file in dir
            'sub/ok.yaml': '---\n'
                           'key: value\n',
            # file in very nested dir
            's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml': '---\n'
                                                       'key: value\n'
                                                       'key: other value\n',
            # empty dir
            'empty-dir': [],
            # non-YAML file
            'no-yaml.json': '---\n'
                            'key: value\n',
            # non-ASCII chars
            'non-ascii/utf-8': (
                u'---\n'
                u'- hétérogénéité\n'
                u'# 19.99 €\n'
                u'- お早う御座います。\n'
                u'# الأَبْجَدِيَّة العَرَبِيَّة\n').encode('utf-8'),
        })

    @classmethod
    def tearDownClass(cls):
        super(CommandLineTestCase, cls).tearDownClass()

        shutil.rmtree(cls.wd)

    def test_find_files_recursively(self):
        conf = config.YamlLintConfig('extends: default')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'a.yaml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'warn.yaml')],
        )

        items = [os.path.join(self.wd, 'sub/ok.yaml'),
                 os.path.join(self.wd, 'empty-dir')]
        self.assertEqual(
            sorted(cli.find_files_recursively(items, conf)),
            [os.path.join(self.wd, 'sub/ok.yaml')],
        )

        items = [os.path.join(self.wd, 'empty.yml'),
                 os.path.join(self.wd, 's')]
        self.assertEqual(
            sorted(cli.find_files_recursively(items, conf)),
            [os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml')],
        )

        items = [os.path.join(self.wd, 'sub'),
                 os.path.join(self.wd, '/etc/another/file')]
        self.assertEqual(
            sorted(cli.find_files_recursively(items, conf)),
            [os.path.join(self.wd, '/etc/another/file'),
             os.path.join(self.wd, 'sub/ok.yaml')],
        )

        conf = config.YamlLintConfig('extends: default\n'
                                     'yaml-files:\n'
                                     '  - \'*.yaml\' \n')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'a.yaml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'warn.yaml')]
        )

        conf = config.YamlLintConfig('extends: default\n'
                                     'yaml-files:\n'
                                     '  - \'*.yml\'\n')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'empty.yml')]
        )

        conf = config.YamlLintConfig('extends: default\n'
                                     'yaml-files:\n'
                                     '  - \'*.json\'\n')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'no-yaml.json')]
        )

        conf = config.YamlLintConfig('extends: default\n'
                                     'yaml-files:\n'
                                     '  - \'*\'\n')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'a.yaml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 'no-yaml.json'),
             os.path.join(self.wd, 'non-ascii/utf-8'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'warn.yaml')]
        )

        conf = config.YamlLintConfig('extends: default\n'
                                     'yaml-files:\n'
                                     '  - \'*.yaml\'\n'
                                     '  - \'*\'\n'
                                     '  - \'**\'\n')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'a.yaml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 'no-yaml.json'),
             os.path.join(self.wd, 'non-ascii/utf-8'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'warn.yaml')]
        )

        conf = config.YamlLintConfig('extends: default\n'
                                     'yaml-files:\n'
                                     '  - \'s/**\'\n'
                                     '  - \'**/utf-8\'\n')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'non-ascii/utf-8')]
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
        self.assertRegexpMatches(
            err.splitlines()[-1],
            r'^yamllint: error: argument -d\/--config-data: '
            r'not allowed with argument -c\/--config-file$'
        )

        # checks if reading from stdin and files are mutually exclusive
        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-', 'file'))

        self.assertNotEqual(ctx.exception.code, 0)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, '')
        self.assertRegexpMatches(err, r'^usage')

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

    def test_run_one_warning(self):
        file = os.path.join(self.wd, 'warn.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-f', 'parsable', file))

        self.assertEqual(ctx.exception.code, 0)

    def test_run_warning_in_strict_mode(self):
        file = os.path.join(self.wd, 'warn.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-f', 'parsable', '--strict', file))

        self.assertEqual(ctx.exception.code, 2)

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

    def test_run_non_ascii_file(self):
        file = os.path.join(self.wd, 'non-ascii', 'utf-8')

        # Make sure the default localization conditions on this "system"
        # support UTF-8 encoding.
        loc = locale.getlocale()
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-f', 'parsable', file))

        locale.setlocale(locale.LC_ALL, loc)

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

    def test_run_piped_output_nocolor(self):
        file = os.path.join(self.wd, 'a.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run((file, ))

        self.assertEqual(ctx.exception.code, 1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, (
            '%s\n'
            '  2:4       error    trailing spaces  (trailing-spaces)\n'
            '  3:4       error    no new line character at the end of file  '
            '(new-line-at-end-of-file)\n'
            '\n' % file))
        self.assertEqual(err, '')

    def test_run_default_format_output_in_tty(self):
        file = os.path.join(self.wd, 'a.yaml')

        # Create a pseudo-TTY and redirect stdout to it
        master, slave = pty.openpty()
        sys.stdout = sys.stderr = os.fdopen(slave, 'w')

        with self.assertRaises(SystemExit) as ctx:
            cli.run((file, ))
        sys.stdout.flush()

        self.assertEqual(ctx.exception.code, 1)

        # Read output from TTY
        output = os.fdopen(master, 'r')
        flag = fcntl.fcntl(master, fcntl.F_GETFD)
        fcntl.fcntl(master, fcntl.F_SETFL, flag | os.O_NONBLOCK)

        out = output.read().replace('\r\n', '\n')

        sys.stdout.close()
        sys.stderr.close()
        output.close()

        self.assertEqual(out, (
            '\033[4m%s\033[0m\n'
            '  \033[2m2:4\033[0m       \033[31merror\033[0m    '
            'trailing spaces  \033[2m(trailing-spaces)\033[0m\n'
            '  \033[2m3:4\033[0m       \033[31merror\033[0m    '
            'no new line character at the end of file  '
            '\033[2m(new-line-at-end-of-file)\033[0m\n'
            '\n' % file))

    def test_run_default_format_output_without_tty(self):
        file = os.path.join(self.wd, 'a.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run((file, ))

        self.assertEqual(ctx.exception.code, 1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, (
            '%s\n'
            '  2:4       error    trailing spaces  (trailing-spaces)\n'
            '  3:4       error    no new line character at the end of file  '
            '(new-line-at-end-of-file)\n'
            '\n' % file))
        self.assertEqual(err, '')

    def test_run_auto_output_without_tty_output(self):
        file = os.path.join(self.wd, 'a.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run((file, '--format', 'auto'))

        self.assertEqual(ctx.exception.code, 1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, (
            '%s\n'
            '  2:4       error    trailing spaces  (trailing-spaces)\n'
            '  3:4       error    no new line character at the end of file  '
            '(new-line-at-end-of-file)\n'
            '\n' % file))
        self.assertEqual(err, '')

    def test_run_format_colored(self):
        file = os.path.join(self.wd, 'a.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run((file, '--format', 'colored'))

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

    def test_run_read_from_stdin(self):
        # prepares stdin with an invalid yaml string so that we can check
        # for its specific error, and be assured that stdin was read
        sys.stdout, sys.stderr = StringIO(), StringIO()
        sys.stdin = StringIO(
            'I am a string\n'
            'therefore: I am an error\n')

        with self.assertRaises(SystemExit) as ctx:
            cli.run(('-', '-f', 'parsable'))

        self.assertNotEqual(ctx.exception.code, 0)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, (
            'stdin:2:10: [error] syntax error: '
            'mapping values are not allowed here (syntax)\n'))
        self.assertEqual(err, '')

    def test_run_no_warnings(self):
        file = os.path.join(self.wd, 'a.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run((file, '--no-warnings', '-f', 'auto'))

        self.assertEqual(ctx.exception.code, 1)

        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        self.assertEqual(out, (
            '%s\n'
            '  2:4       error    trailing spaces  (trailing-spaces)\n'
            '  3:4       error    no new line character at the end of file  '
            '(new-line-at-end-of-file)\n'
            '\n' % file))
        self.assertEqual(err, '')

        file = os.path.join(self.wd, 'warn.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run((file, '--no-warnings', '-f', 'auto'))

        self.assertEqual(ctx.exception.code, 0)

    def test_run_no_warnings_and_strict(self):
        file = os.path.join(self.wd, 'warn.yaml')

        sys.stdout, sys.stderr = StringIO(), StringIO()
        with self.assertRaises(SystemExit) as ctx:
            cli.run((file, '--no-warnings', '-s'))

        self.assertEqual(ctx.exception.code, 2)
