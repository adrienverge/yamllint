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

import glob
import locale
import os
import pty
import shutil
import sys
import tempfile
import unittest

from tests.common import (
    RunContext,
    build_temp_workspace,
    register_test_codecs,
    temp_workspace,
    temp_workspace_with_files_in_many_codecs,
    unregister_test_codecs
)

from yamllint import cli, config


# Check system's UTF-8 availability
def utf8_available():
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        locale.setlocale(locale.LC_ALL, (None, None))
    except locale.Error:  # pragma: no cover
        return False
    else:
        return True


class CommandLineTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

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
            # directory that looks like a yaml file
            'sub/directory.yaml/not-yaml.txt': '',
            'sub/directory.yaml/empty.yml': '',
            # file in very nested dir
            's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml': '---\n'
                                                       'key: value\n'
                                                       'key: other value\n',
            # empty dir
            'empty-dir': [],
            # symbolic link
            'symlinks/file-without-yaml-extension': '42\n',
            'symlinks/link.yaml': 'symlink://file-without-yaml-extension',
            # non-YAML file
            'no-yaml.json': '---\n'
                            'key: value\n',
            # non-ASCII chars
            'non-ascii/éçäγλνπ¥/utf-8': (
                '---\n'
                '- hétérogénéité\n'
                '# 19.99 €\n'
                '- お早う御座います。\n'
                '# الأَبْجَدِيَّة العَرَبِيَّة\n').encode(),
            # dos line endings yaml
            'dos.yml': '---\r\n'
                       'dos: true',
            # different key-ordering by locale
            'c.yaml': '---\n'
                      'A: true\n'
                      'a: true',
            'en.yaml': '---\n'
                       'a: true\n'
                       'A: true'
        })

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        shutil.rmtree(cls.wd)

    def test_find_files_recursively(self):
        conf = config.YamlLintConfig('extends: default')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'a.yaml'),
             os.path.join(self.wd, 'c.yaml'),
             os.path.join(self.wd, 'dos.yml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 'en.yaml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/directory.yaml/empty.yml'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'symlinks/link.yaml'),
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
             os.path.join(self.wd, 'sub/directory.yaml/empty.yml'),
             os.path.join(self.wd, 'sub/ok.yaml')],
        )

        conf = config.YamlLintConfig('extends: default\n'
                                     'yaml-files:\n'
                                     '  - \'*.yaml\' \n')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'a.yaml'),
             os.path.join(self.wd, 'c.yaml'),
             os.path.join(self.wd, 'en.yaml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'symlinks/link.yaml'),
             os.path.join(self.wd, 'warn.yaml')]
        )

        conf = config.YamlLintConfig('extends: default\n'
                                     'yaml-files:\n'
                                     '  - \'*.yml\'\n')
        self.assertEqual(
            sorted(cli.find_files_recursively([self.wd], conf)),
            [os.path.join(self.wd, 'dos.yml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 'sub/directory.yaml/empty.yml')]
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
             os.path.join(self.wd, 'c.yaml'),
             os.path.join(self.wd, 'dos.yml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 'en.yaml'),
             os.path.join(self.wd, 'no-yaml.json'),
             os.path.join(self.wd, 'non-ascii/éçäγλνπ¥/utf-8'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/directory.yaml/empty.yml'),
             os.path.join(self.wd, 'sub/directory.yaml/not-yaml.txt'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'symlinks/file-without-yaml-extension'),
             os.path.join(self.wd, 'symlinks/link.yaml'),
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
             os.path.join(self.wd, 'c.yaml'),
             os.path.join(self.wd, 'dos.yml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 'en.yaml'),
             os.path.join(self.wd, 'no-yaml.json'),
             os.path.join(self.wd, 'non-ascii/éçäγλνπ¥/utf-8'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/directory.yaml/empty.yml'),
             os.path.join(self.wd, 'sub/directory.yaml/not-yaml.txt'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'symlinks/file-without-yaml-extension'),
             os.path.join(self.wd, 'symlinks/link.yaml'),
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
        self.assertRegex(ctx.stderr, r'^usage')

        with RunContext(self) as ctx:
            cli.run(('--unknown-arg', ))
        self.assertNotEqual(ctx.returncode, 0)
        self.assertEqual(ctx.stdout, '')
        self.assertRegex(ctx.stderr, r'^usage')

        with RunContext(self) as ctx:
            cli.run(('-c', './conf.yaml', '-d', 'relaxed', 'file'))
        self.assertNotEqual(ctx.returncode, 0)
        self.assertEqual(ctx.stdout, '')
        self.assertRegex(
            ctx.stderr.splitlines()[-1],
            r'^yamllint: error: argument -d\/--config-data: '
            r'not allowed with argument -c\/--config-file$'
        )

        # checks if reading from stdin and files are mutually exclusive
        with RunContext(self) as ctx:
            cli.run(('-', 'file'))
        self.assertNotEqual(ctx.returncode, 0)
        self.assertEqual(ctx.stdout, '')
        self.assertRegex(ctx.stderr, r'^usage')

    def test_run_with_bad_config(self):
        with RunContext(self) as ctx:
            cli.run(('-d', 'rules: {a: b}', 'file'))
        self.assertEqual(ctx.returncode, -1)
        self.assertEqual(ctx.stdout, '')
        self.assertRegex(ctx.stderr, r'^invalid config: no such rule')

    def test_run_with_empty_config(self):
        with RunContext(self) as ctx:
            cli.run(('-d', '', 'file'))
        self.assertEqual(ctx.returncode, -1)
        self.assertEqual(ctx.stdout, '')
        self.assertRegex(ctx.stderr, r'^invalid config: not a dict')

    def test_run_with_implicit_extends_config(self):
        path = os.path.join(self.wd, 'warn.yaml')

        with RunContext(self) as ctx:
            cli.run(('-d', 'default', '-f', 'parsable', path))
        expected_out = (f'{path}:1:1: [warning] missing document start "---" '
                        f'(document-start)\n')
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (0, expected_out, ''))

    def test_run_with_config_file(self):
        with open(os.path.join(self.wd, 'config'), 'w', encoding='utf_8') as f:
            f.write('rules: {trailing-spaces: disable}')

        with RunContext(self) as ctx:
            cli.run(('-c', f.name, os.path.join(self.wd, 'a.yaml')))
        self.assertEqual(ctx.returncode, 0)

        with open(os.path.join(self.wd, 'config'), 'w', encoding='utf_8') as f:
            f.write('rules: {trailing-spaces: enable}')

        with RunContext(self) as ctx:
            cli.run(('-c', f.name, os.path.join(self.wd, 'a.yaml')))
        self.assertEqual(ctx.returncode, 1)

    def test_run_with_user_global_config_file(self):
        home = os.path.join(self.wd, 'fake-home')
        dir = os.path.join(home, '.config', 'yamllint')
        os.makedirs(dir)
        config = os.path.join(dir, 'config')

        self.addCleanup(os.environ.__delitem__, 'HOME')
        os.environ['HOME'] = home

        with open(config, 'w', encoding='utf_8') as f:
            f.write('rules: {trailing-spaces: disable}')

        with RunContext(self) as ctx:
            cli.run((os.path.join(self.wd, 'a.yaml'), ))
        self.assertEqual(ctx.returncode, 0)

        with open(config, 'w', encoding='utf_8') as f:
            f.write('rules: {trailing-spaces: enable}')

        with RunContext(self) as ctx:
            cli.run((os.path.join(self.wd, 'a.yaml'), ))
        self.assertEqual(ctx.returncode, 1)

    def test_run_with_user_xdg_config_home_in_env(self):
        self.addCleanup(os.environ.__delitem__, 'XDG_CONFIG_HOME')

        with tempfile.TemporaryDirectory('w') as d:
            os.environ['XDG_CONFIG_HOME'] = d
            os.makedirs(os.path.join(d, 'yamllint'))
            path = os.path.join(d, 'yamllint', 'config')
            with open(path, 'w', encoding='utf_8') as f:
                f.write('extends: relaxed')
            with RunContext(self) as ctx:
                cli.run(('-f', 'parsable', os.path.join(self.wd, 'warn.yaml')))

        self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr), (0, '', ''))

    def test_run_with_user_yamllint_config_file_in_env(self):
        self.addCleanup(os.environ.__delitem__, 'YAMLLINT_CONFIG_FILE')

        with tempfile.NamedTemporaryFile('w', encoding='utf_8') as f:
            os.environ['YAMLLINT_CONFIG_FILE'] = f.name
            f.write('rules: {trailing-spaces: disable}')
            f.flush()
            with RunContext(self) as ctx:
                cli.run((os.path.join(self.wd, 'a.yaml'), ))
            self.assertEqual(ctx.returncode, 0)

        with tempfile.NamedTemporaryFile('w', encoding='utf_8') as f:
            os.environ['YAMLLINT_CONFIG_FILE'] = f.name
            f.write('rules: {trailing-spaces: enable}')
            f.flush()
            with RunContext(self) as ctx:
                cli.run((os.path.join(self.wd, 'a.yaml'), ))
            self.assertEqual(ctx.returncode, 1)

    def test_run_with_locale(self):
        # check for availability of locale, otherwise skip the test
        # reset to default before running the test,
        # as the first two runs don't use setlocale()
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except locale.Error:  # pragma: no cover
            self.skipTest('locale en_US.UTF-8 not available')
        locale.setlocale(locale.LC_ALL, (None, None))

        # C + en.yaml should fail
        with RunContext(self) as ctx:
            cli.run(('-d', 'rules: { key-ordering: enable }',
                     os.path.join(self.wd, 'en.yaml')))
        self.assertEqual(ctx.returncode, 1)

        # C + c.yaml should pass
        with RunContext(self) as ctx:
            cli.run(('-d', 'rules: { key-ordering: enable }',
                    os.path.join(self.wd, 'c.yaml')))
        self.assertEqual(ctx.returncode, 0)

        # the next two runs use setlocale() inside,
        # so we need to clean up afterwards
        self.addCleanup(locale.setlocale, locale.LC_ALL, (None, None))

        # en_US + en.yaml should pass
        with RunContext(self) as ctx:
            cli.run(('-d', 'locale: en_US.UTF-8\n'
                           'rules: { key-ordering: enable }',
                     os.path.join(self.wd, 'en.yaml')))
        self.assertEqual(ctx.returncode, 0)

        # en_US + c.yaml should fail
        with RunContext(self) as ctx:
            cli.run(('-d', 'locale: en_US.UTF-8\n'
                           'rules: { key-ordering: enable }',
                     os.path.join(self.wd, 'c.yaml')))
        self.assertEqual(ctx.returncode, 1)

    def test_run_version(self):
        with RunContext(self) as ctx:
            cli.run(('--version', ))
        self.assertEqual(ctx.returncode, 0)
        self.assertRegex(ctx.stdout + ctx.stderr, r'yamllint \d+\.\d+')

    def test_run_non_existing_file(self):
        path = os.path.join(self.wd, 'i-do-not-exist.yaml')

        with RunContext(self) as ctx:
            cli.run(('-f', 'parsable', path))
        self.assertEqual(ctx.returncode, -1)
        self.assertEqual(ctx.stdout, '')
        self.assertRegex(ctx.stderr, r'No such file or directory')

    def test_run_one_problem_file(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run(('-f', 'parsable', path))
        self.assertEqual(ctx.returncode, 1)
        self.assertEqual(ctx.stdout, (
            f'{path}:2:4: [error] trailing spaces (trailing-spaces)\n'
            f'{path}:3:4: [error] no new line character at the end of file '
            f'(new-line-at-end-of-file)\n'))
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

    @unittest.skipIf(not utf8_available(), 'C.UTF-8 not available')
    def test_run_non_ascii_file(self):
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        self.addCleanup(locale.setlocale, locale.LC_ALL, (None, None))

        path = os.path.join(self.wd, 'non-ascii', 'éçäγλνπ¥', 'utf-8')
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
            f'{path}:3:1: [error] duplication of key "key" in mapping '
            f'(key-duplicates)\n'))

    def test_run_piped_output_nocolor(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, ))
        self.assertEqual((ctx.returncode, ctx.stderr), (1, ''))
        self.assertEqual(ctx.stdout, (
            f'{path}\n'
            f'  2:4       error    trailing spaces  (trailing-spaces)\n'
            f'  3:4       error    no new line character at the end of file  '
            f'(new-line-at-end-of-file)\n'
            f'\n'))

    def test_run_default_format_output_in_tty(self):
        path = os.path.join(self.wd, 'a.yaml')

        # Create a pseudo-TTY and redirect stdout to it
        old_stdout = sys.stdout
        master, slave = pty.openpty()
        sys.stdout = os.fdopen(
            slave,
            'w',
            encoding=os.device_encoding(slave)
        )

        with self.assertRaises(SystemExit) as ctx:
            cli.run((path, ))
        sys.stdout.flush()

        self.assertEqual(ctx.exception.code, 1)

        # Read output from TTY
        output = os.fdopen(master, 'r', encoding=os.device_encoding(master))
        os.set_blocking(master, False)

        out = output.read().replace('\r\n', '\n')

        sys.stdout.close()
        output.close()
        sys.stdout = old_stdout

        self.assertEqual(out, (
            f'\033[4m{path}\033[0m\n'
            f'  \033[2m2:4\033[0m       \033[31merror\033[0m    '
            f'trailing spaces  \033[2m(trailing-spaces)\033[0m\n'
            f'  \033[2m3:4\033[0m       \033[31merror\033[0m    '
            f'no new line character at the end of file  '
            f'\033[2m(new-line-at-end-of-file)\033[0m\n'
            f'\n'))

    def test_run_default_format_output_without_tty(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, ))
        expected_out = (
            f'{path}\n'
            f'  2:4       error    trailing spaces  (trailing-spaces)\n'
            f'  3:4       error    no new line character at the end of file  '
            f'(new-line-at-end-of-file)\n'
            f'\n')
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_run_auto_output_without_tty_output(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--format', 'auto'))
        expected_out = (
            f'{path}\n'
            f'  2:4       error    trailing spaces  (trailing-spaces)\n'
            f'  3:4       error    no new line character at the end of file  '
            f'(new-line-at-end-of-file)\n'
            f'\n')
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_run_format_colored(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--format', 'colored'))
        expected_out = (
            f'\033[4m{path}\033[0m\n'
            f'  \033[2m2:4\033[0m       \033[31merror\033[0m    '
            f'trailing spaces  \033[2m(trailing-spaces)\033[0m\n'
            f'  \033[2m3:4\033[0m       \033[31merror\033[0m    '
            f'no new line character at the end of file  '
            f'\033[2m(new-line-at-end-of-file)\033[0m\n'
            f'\n')
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_run_format_colored_warning(self):
        path = os.path.join(self.wd, 'warn.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--format', 'colored'))
        expected_out = (
            f'\033[4m{path}\033[0m\n'
            f'  \033[2m1:1\033[0m       \033[33mwarning\033[0m  '
            f'missing document start "---"  \033[2m(document-start)\033[0m\n'
            f'\n')
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (0, expected_out, ''))

    def test_run_format_github(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--format', 'github'))
        expected_out = (
            f'::group::{path}\n'
            f'::error file={path},line=2,col=4::2:4 [trailing-spaces] trailing'
            f' spaces\n'
            f'::error file={path},line=3,col=4::3:4 [new-line-at-end-of-file]'
            f' no new line character at the end of file\n'
            f'::endgroup::\n\n')
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_github_actions_detection(self):
        path = os.path.join(self.wd, 'a.yaml')
        self.addCleanup(os.environ.__delitem__, 'GITHUB_ACTIONS')
        self.addCleanup(os.environ.__delitem__, 'GITHUB_WORKFLOW')

        with RunContext(self) as ctx:
            os.environ['GITHUB_ACTIONS'] = 'something'
            os.environ['GITHUB_WORKFLOW'] = 'something'
            cli.run((path, ))
        expected_out = (
            f'::group::{path}\n'
            f'::error file={path},line=2,col=4::2:4 [trailing-spaces] trailing'
            f' spaces\n'
            f'::error file={path},line=3,col=4::3:4 [new-line-at-end-of-file]'
            f' no new line character at the end of file\n'
            f'::endgroup::\n\n')
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_run_read_from_stdin(self):
        self.addCleanup(setattr, sys, 'stdin', sys.__stdin__)
        # Normally, I would just use tempfile.TemporaryFile(), but here I want
        # to first open the file for writing and then open it for reading. In
        # other words, I need to make sure that the file continues to exist
        # after I close it for the fist time. That’s why I’m using
        # tempfile.TemporaryDirectory() instead of tempfile.TemporaryFile().
        with tempfile.TemporaryDirectory() as temp_dir_path:
            stdin_file_path = os.path.join(temp_dir_path, 'stdin')
            with open(stdin_file_path, mode='w', encoding='utf_8') as file:
                file.write(
                    'I am a string\n'
                    'therefore: I am an error\n')
            with open(stdin_file_path, mode='r', encoding='utf-8') as file:
                # prepares stdin with an invalid yaml string so that we can
                # check for its specific error, and be assured that stdin was
                # read
                sys.stdin = file

                with RunContext(self) as ctx:
                    cli.run(('-', '-f', 'parsable'))
                expected_out = (
                    'stdin:2:10: [error] syntax error: '
                    'mapping values are not allowed here (syntax)\n')
                self.assertEqual(
                    (ctx.returncode, ctx.stdout, ctx.stderr),
                    (1, expected_out, ''))

    def test_run_no_warnings(self):
        path = os.path.join(self.wd, 'a.yaml')

        with RunContext(self) as ctx:
            cli.run((path, '--no-warnings', '-f', 'auto'))
        expected_out = (
            f'{path}\n'
            f'  2:4       error    trailing spaces  (trailing-spaces)\n'
            f'  3:4       error    no new line character at the end of file  '
            f'(new-line-at-end-of-file)\n'
            f'\n')
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
            f'{path}\n'
            f'  1:4       error    wrong new line character: expected \\n'
            f'  (new-lines)\n'
            f'\n')
        self.assertEqual(
            (ctx.returncode, ctx.stdout, ctx.stderr), (1, expected_out, ''))

    def test_run_list_files(self):
        with RunContext(self) as ctx:
            cli.run(('--list-files', self.wd))
        self.assertEqual(ctx.returncode, 0)
        self.assertEqual(
            sorted(ctx.stdout.splitlines()),
            [os.path.join(self.wd, 'a.yaml'),
             os.path.join(self.wd, 'c.yaml'),
             os.path.join(self.wd, 'dos.yml'),
             os.path.join(self.wd, 'empty.yml'),
             os.path.join(self.wd, 'en.yaml'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/directory.yaml/empty.yml'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'symlinks/link.yaml'),
             os.path.join(self.wd, 'warn.yaml')]
        )

        config = '{ignore: "*.yml", yaml-files: ["*.*"]}'
        with RunContext(self) as ctx:
            cli.run(('--list-files', '-d', config, self.wd))
        self.assertEqual(ctx.returncode, 0)
        self.assertEqual(
            sorted(ctx.stdout.splitlines()),
            [os.path.join(self.wd, 'a.yaml'),
             os.path.join(self.wd, 'c.yaml'),
             os.path.join(self.wd, 'en.yaml'),
             os.path.join(self.wd, 'no-yaml.json'),
             os.path.join(self.wd, 's/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file.yaml'),
             os.path.join(self.wd, 'sub/directory.yaml/not-yaml.txt'),
             os.path.join(self.wd, 'sub/ok.yaml'),
             os.path.join(self.wd, 'symlinks/link.yaml'),
             os.path.join(self.wd, 'warn.yaml')]
        )

        config = 'ignore: ["*.yaml", "*.yml", "!a.yaml"]'
        with RunContext(self) as ctx:
            cli.run(('--list-files', '-d', config, self.wd))
        self.assertEqual(ctx.returncode, 0)
        self.assertEqual(
            sorted(ctx.stdout.splitlines()),
            [os.path.join(self.wd, 'a.yaml')]
        )
        with RunContext(self) as ctx:
            cli.run(('--list-files', '-d', config,
                     os.path.join(self.wd, 'a.yaml'),
                     os.path.join(self.wd, 'en.yaml'),
                     os.path.join(self.wd, 'c.yaml')))
        self.assertEqual(ctx.returncode, 0)
        self.assertEqual(
            sorted(ctx.stdout.splitlines()),
            [os.path.join(self.wd, 'a.yaml')]
        )


class CommandLineConfigTestCase(unittest.TestCase):
    def test_config_file(self):
        workspace = {'a.yml': 'hello: world\n'}
        conf = ('---\n'
                'extends: relaxed\n')

        for conf_file in ('.yamllint', '.yamllint.yml', '.yamllint.yaml'):
            with self.subTest(conf_file):
                with temp_workspace(workspace):
                    with RunContext(self) as ctx:
                        cli.run(('-f', 'parsable', '.'))

                self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr),
                                 (0, './a.yml:1:1: [warning] missing document '
                                     'start "---" (document-start)\n', ''))

                with temp_workspace({**workspace, conf_file: conf}):
                    with RunContext(self) as ctx:
                        cli.run(('-f', 'parsable', '.'))

                self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr),
                                 (0, '', ''))

    def test_parent_config_file(self):
        workspace = {'a/b/c/d/e/f/g/a.yml': 'hello: world\n'}
        conf = ('---\n'
                'extends: relaxed\n')

        for conf_file in ('.yamllint', '.yamllint.yml', '.yamllint.yaml'):
            with self.subTest(conf_file):
                with temp_workspace(workspace):
                    with RunContext(self) as ctx:
                        os.chdir('a/b/c/d/e/f')
                        cli.run(('-f', 'parsable', '.'))

                self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr),
                                 (0, './g/a.yml:1:1: [warning] missing '
                                     'document start "---" (document-start)\n',
                                     ''))

                with temp_workspace({**workspace, conf_file: conf}):
                    with RunContext(self) as ctx:
                        os.chdir('a/b/c/d/e/f')
                        cli.run(('-f', 'parsable', '.'))

                self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr),
                                 (0, '', ''))

    def test_multiple_parent_config_file(self):
        workspace = {'a/b/c/3spaces.yml': 'array:\n'
                                          '   - item\n',
                     'a/b/c/4spaces.yml': 'array:\n'
                                          '    - item\n',
                     'a/.yamllint': '---\n'
                                    'extends: relaxed\n'
                                    'rules:\n'
                                    '  indentation:\n'
                                    '    spaces: 4\n',
                     }

        conf3 = ('---\n'
                 'extends: relaxed\n'
                 'rules:\n'
                 '  indentation:\n'
                 '    spaces: 3\n')

        with temp_workspace(workspace):
            with RunContext(self) as ctx:
                os.chdir('a/b/c')
                cli.run(('-f', 'parsable', '.'))

        self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr),
                         (0, './3spaces.yml:2:4: [warning] wrong indentation: '
                         'expected 4 but found 3 (indentation)\n', ''))

        with temp_workspace({**workspace, 'a/b/.yamllint.yml': conf3}):
            with RunContext(self) as ctx:
                os.chdir('a/b/c')
                cli.run(('-f', 'parsable', '.'))

        self.assertEqual((ctx.returncode, ctx.stdout, ctx.stderr),
                         (0, './4spaces.yml:2:5: [warning] wrong indentation: '
                         'expected 3 but found 4 (indentation)\n', ''))


class CommandLineEncodingTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        register_test_codecs()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        unregister_test_codecs()

    def valid_encodings_stdin_test_helper(
        self,
        config_path,
        root_dir,
        old_stdin
    ):
        for path in glob.glob(os.path.join(root_dir, '**')):
            # We purposely choose the wrong text encoding here because the text
            # encoding shouldn’t matter. yamllint should completely ignore the
            # text encoding of stdin.
            with open(path, mode="r", encoding="cp037") as file:
                sys.stdin = file
                with RunContext(self) as ctx:
                    cli.run(('-c', config_path, '-'))
                sys.stdin = old_stdin
                if root_dir == 'sorted_correctly':
                    self.assertEqual(ctx.returncode, 0)
                elif root_dir == 'sorted_incorrectly':
                    self.assertNotEqual(ctx.returncode, 0)
                else:
                    raise ValueError(
                        f"root_dir was set to {repr(root_dir)}. It should only"
                        "ever be set to 'sorted_correctly' or"
                        "'sorted_incorrectly'."
                    )

    def test_valid_encodings(self):
        old_stdin = sys.stdin
        self.addCleanup(setattr, sys, 'stdin', old_stdin)
        conf = ('---\n'
                'rules:\n'
                '  key-ordering: enable\n')
        config_files = temp_workspace_with_files_in_many_codecs(
            'config_{}.yaml',
            conf
        )
        sorted_correctly = ('---\n'
                            'Ａ: YAML\n'
                            'Ｚ: YAML\n')
        sorted_correctly_files = temp_workspace_with_files_in_many_codecs(
            'sorted_correctly/{}.yaml',
            sorted_correctly
        )
        sorted_incorrectly = ('---\n'
                              'Ｚ: YAML\n'
                              'Ａ: YAML\n')
        sorted_incorrectly_files = temp_workspace_with_files_in_many_codecs(
            'sorted_incorrectly/{}.yaml',
            sorted_incorrectly
        )
        workspace = {
            **config_files,
            **sorted_correctly_files,
            **sorted_incorrectly_files
        }

        with temp_workspace(workspace):
            for config_path in config_files.keys():
                # First, make sure that encoding autodetection works when the
                # file’s path is given as a command-line argument.
                with RunContext(self) as ctx:
                    cli.run(('-c', config_path, 'sorted_correctly'))
                self.assertEqual(ctx.returncode, 0)
                with RunContext(self) as ctx:
                    cli.run(('-c', config_path, 'sorted_incorrectly'))
                self.assertNotEqual(ctx.returncode, 0)
                # Second, make sure that encoding autodetection works when the
                # file is piped to yamllint via stdin.
                self.valid_encodings_stdin_test_helper(
                    config_path,
                    'sorted_correctly',
                    old_stdin
                )
                self.valid_encodings_stdin_test_helper(
                    config_path,
                    'sorted_incorrectly',
                    old_stdin
                )
