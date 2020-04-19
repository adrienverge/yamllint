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


class RunContext(object):
    """Context manager for ``cli.run()`` to capture exit code and streams."""

    def __init__(self, case):
        self.stdout = self.stderr = None
        self._raises_ctx = case.assertRaises(SystemExit)

    def __enter__(self):
        self._raises_ctx.__enter__()
        sys.stdout = self.outstream = StringIO()
        sys.stderr = self.errstream = StringIO()
        return self

    def __exit__(self, *exc_info):
        self.stdout, sys.stdout = self.outstream.getvalue(), sys.__stdout__
        self.stderr, sys.stderr = self.errstream.getvalue(), sys.__stderr__
        return self._raises_ctx.__exit__(*exc_info)

    @property
    def returncode(self):
        return self._raises_ctx.exception.code


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
            'non-ascii/éçäγλνπ¥/utf-8': (
                u'---\n'
                u'- hétérogénéité\n'
                u'# 19.99 €\n'
                u'- お早う御座います。\n'
                u'# الأَبْجَدِيَّة العَرَبِيَّة\n').encode('utf-8'),
            # dos line endings yaml
            'dos.yml': '---\r\n'
                       'dos: true',
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
             os.path.join(self.wd, 'dos.yml'),
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
            [os.path.join(self.wd, 'dos.yml'),
             os.path.join(self.wd, 'empty.yml')]
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
             os.path.join(self.wd, 'dos.yml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 'no-yaml.json'),
             os.path.join(self.wd, 'non-ascii/éçäγλνπ¥/utf-8'),
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
             os.path.join(self.wd, 'dos.yml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 'no-yaml.json'),
             os.path.join(self.wd, 'non-ascii/éçäγλνπ¥/utf-8'),
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
            [os.path.join(self.wd, 'non-ascii/éçäγλνπ¥/utf-8')]
        )

    def test_run_with_bad_arguments(self):
        with RunContext(self) as ctx:
            cli.run(())
        self.assertNotEqual(ctx.returncode, 0)
        self.assertEqual(ctx.stdout, '')
        self.assertRegexpMatches(ctx.stderr, r'^usage')

        with RunContext(self) as ctx:
            cli.run(('--unknown-arg', ))
        self.assertNotEqual(ctx.returncode, 0)
        self.assertEqual(ctx.stdout, '')
        self.assertRegexpMatches(ctx.stderr, r'^usage')

        with RunContext(self) as ctx:
            cli.run(('-c', './conf.yaml', '-d', 'relaxed', 'file'))
        self.assertNotEqual(ctx.returncode, 0)
        self.assertEqual(ctx.stdout, '')
        self.assertRegexpMatches(
            ctx.stderr.splitlines()[-1],
            r'^yamllint: error: argument -d\/--config-data: '
            r'not allowed with argument -c\/--config-file$'
        )

        # checks if reading from stdin and files are mutually exclusive
        with RunContext(self) as ctx:
            cli.run(('-', 'file'))
        self.assertNotEqual(ctx.returncode, 0)
        self.assertEqual(ctx.stdout, '')
        self.assertRegexpMatches(ctx.stderr, r'^usage')

    def test_run_with_bad_config(self):
        with RunContext(self) as ctx:
            cli.run(('-d', 'rules: {a: b}', 'file'))
        self.assertEqual(ctx.returncode, -1)
        self.assertEqual(ctx.stdout, '')
        self.assertRegexpMatches(ctx.stderr, r'^invalid config: no such rule')

    def test_run_with_empty_config(self):
        with RunContext(self) as ctx:
            cli.run(('-d', '', 'file'))
        self.assertEqual(ctx.returncode, -1)
        self.assertEqual(ctx.stdout, '')
        self.assertRegexpMatches(ctx.stderr, r'^invalid config: not a dict')

    def test_run_with_config_file(self):
        with open(os.path.join(self.wd, 'config'), 'w') as f:
            f.write('rules: {trailing-spaces: disable}')

        with RunContext(self) as ctx:
            cli.run(('-c', f.name, os.path.join(self.wd, 'a.yaml')))
        self.assertEqual(ctx.returncode, 0)

        with open(os.path.join(self.wd, 'config'), 'w') as f:
            f.write('rules: {trailing-spaces: enable}')

        with RunContext(self) as ctx:
            cli.run(('-c', f.name, os.path.join(self.wd, 'a.yaml')))
        self.assertEqual(ctx.returncode, 1)

    def test_run_with_user_global_config_file(self):
        home = os.path.join(self.wd, 'fake-home')
        dir = os.path.join(home, '.config', 'yamllint')
        os.makedirs(dir)
        config = os.path.join(dir, 'config')

        self.addCleanup(os.environ.update, HOME=os.environ['HOME'])
        os.environ['HOME'] = home

        with open(config, 'w') as f:
            f.write('rules: {trailing-spaces: disable}')

        with RunContext(self) as ctx:
            cli.run((os.path.join(self.wd, 'a.yaml'), ))
        self.assertEqual(ctx.returncode, 0)

        with open(config, 'w') as f:
            f.write('rules: {trailing-spaces: enable}')

        with RunContext(self) as ctx:
            cli.run((os.path.join(self.wd, 'a.yaml'), ))
        self.assertEqual(ctx.returncode, 1)

    def test_run_version(self):
        with RunContext(self) as ctx:
            cli.run(('--version', ))
        self.assertEqual(ctx.returncode, 0)
        self.assertRegexpMatches(ctx.stdout + ctx.stderr, r'yamllint \d+\.\d+')

    def test_run_non_existing_file(self):
        path = os.path.join(self.wd, 'i-do-not-exist.yaml')

        with RunContext(self) as ctx:
            cli.run(('-f', 'parsable', path))
        self.assertEqual(ctx.returncode, -1)
        self.assertEqual(ctx.stdout, '')
        self.assertRegexpMatches(ctx.stderr, r'No such file or directory')

    def test_run_one_problem_file(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run(('-f', 'parsable', path))
        self.assertEqual(ctx.returncode, 1)
        self.assertEqual(ctx.stdout, (
            '%s:2:4: [error] trailing spaces (trailing-spaces)\n'
            '%s:3:4: [error] no new line character at the end of file '
            '(new-line-at-end-of-file)\n' % (path, path)))
        self.assertEqual(ctx.stderr, '')

    def test_run_one_warning(self):
        path = os.path.join(self.wd, 'warn.yaml')

        with RunContext(self) as ctx:
            cli.run(('-f', 'parsable', path))
        self.assertEqual(ctx.returncode, 0)

    def test_run_warning_in_strict_mode(self):
        path = os.path.join(self.wd, 'warn.yaml')

        with RunContext(self) as ctx:
            cli.run(('-f', 'parsable', '--strict', path))
        self.assertEqual(ctx.returncode, 2)

    def test_run_one_ok_file(self):
        path = os.path.join(self.wd, 'sub', 'ok.yaml')

        with RunContext(self) as ctx:
            cli.run(('-f', 'parsable', path))
        self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr), (0, '', ''))

    def test_run_empty_file(self):
        path = os.path.join(self.wd, 'empty.yml')

        with RunContext(self) as ctx:
            cli.run(('-f', 'parsable', path))
        self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr), (0, '', ''))

    def test_run_non_ascii_file(self):
        path = os.path.join(self.wd, 'non-ascii', 'éçäγλνπ¥', 'utf-8')

        # Make sure the default localization conditions on this "system"
        # support UTF-8 encoding.
        loc = locale.getlocale()
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        self.addCleanup(locale.setlocale, locale.LC_ALL, loc)

        with RunContext(self) as ctx:
            cli.run(('-f', 'parsable', path))
        self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr), (0, '', ''))

    def test_run_multiple_files(self):
        items = [os.path.join(self.wd, 'empty.yml'),
                 os.path.join(self.wd, 's')]
        path = items[1] + '/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'

        with RunContext(self) as ctx:
            cli.run(['-f', 'parsable'] + items)
        self.assertEqual((ctx.returncode, ctx.stderr), (1, ''))
        self.assertEqual(ctx.stdout, (
            '%s:3:1: [error] duplication of key "key" in mapping '
            '(key-duplicates)\n') % path)

    def test_run_piped_output_nocolor(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, ))
        self.assertEqual((ctx.returncode, ctx.stderr), (1, ''))
        self.assertEqual(ctx.stdout, (
            '%s\n'
            '  2:4       error    trailing spaces  (trailing-spaces)\n'
            '  3:4       error    no new line character at the end of file  '
            '(new-line-at-end-of-file)\n'
            '\n' % path))

    def test_run_default_format_output_in_tty(self):
        path = os.path.join(self.wd, 'a.yaml')

        # Create a pseudo-TTY and redirect stdout to it
        master, slave = pty.openpty()
        sys.stdout = sys.stderr = os.fdopen(slave, 'w')

        with self.assertRaises(SystemExit) as ctx:
            cli.run((path, ))
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
            '\n' % path))

    def test_run_default_format_output_without_tty(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, ))
        expected_out = (
            '%s\n'
            '  2:4       error    trailing spaces  (trailing-spaces)\n'
            '  3:4       error    no new line character at the end of file  '
            '(new-line-at-end-of-file)\n'
            '\n' % path)
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_run_auto_output_without_tty_output(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--format', 'auto'))
        expected_out = (
            '%s\n'
            '  2:4       error    trailing spaces  (trailing-spaces)\n'
            '  3:4       error    no new line character at the end of file  '
            '(new-line-at-end-of-file)\n'
            '\n' % path)
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_run_format_colored(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--format', 'colored'))
        expected_out = (
            '\033[4m%s\033[0m\n'
            '  \033[2m2:4\033[0m       \033[31merror\033[0m    '
            'trailing spaces  \033[2m(trailing-spaces)\033[0m\n'
            '  \033[2m3:4\033[0m       \033[31merror\033[0m    '
            'no new line character at the end of file  '
            '\033[2m(new-line-at-end-of-file)\033[0m\n'
            '\n' % path)
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_run_read_from_stdin(self):
        # prepares stdin with an invalid yaml string so that we can check
        # for its specific error, and be assured that stdin was read
        self.addCleanup(setattr, sys, 'stdin', sys.__stdin__)
        sys.stdin = StringIO(
            'I am a string\n'
            'therefore: I am an error\n')

        with RunContext(self) as ctx:
            cli.run(('-', '-f', 'parsable'))
        expected_out = (
            'stdin:2:10: [error] syntax error: '
            'mapping values are not allowed here (syntax)\n')
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_run_no_warnings(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--no-warnings', '-f', 'auto'))
        expected_out = (
            '%s\n'
            '  2:4       error    trailing spaces  (trailing-spaces)\n'
            '  3:4       error    no new line character at the end of file  '
            '(new-line-at-end-of-file)\n'
            '\n' % path)
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

        path = os.path.join(self.wd, 'warn.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--no-warnings', '-f', 'auto'))
        self.assertEqual(ctx.returncode, 0)

    def test_run_no_warnings_and_strict(self):
        path = os.path.join(self.wd, 'warn.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--no-warnings', '-s'))
        self.assertEqual(ctx.returncode, 2)

    def test_run_non_universal_newline(self):
        path = os.path.join(self.wd, 'dos.yml')

        with RunContext(self) as ctx:
            cli.run(('-d', 'rules:\n  new-lines:\n    type: dos', path))
        self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr), (0, '', ''))

        with RunContext(self) as ctx:
            cli.run(('-d', 'rules:\n  new-lines:\n    type: unix', path))
        expected_out = (
            '%s\n'
            '  1:4       error    wrong new line character: expected \\n'
            '  (new-lines)\n'
            '\n' % path)
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))
