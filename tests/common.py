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

import contextlib
from io import StringIO
import os
import shutil
import sys
import tempfile
import unittest

import yaml

from yamllint import linter
from yamllint.config import YamlLintConfig


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


def build_temp_workspace(files):
    tempdir = tempfile.mkdtemp(prefix='yamllint-tests-')

    for path, content in files.items():
        path = os.path.join(tempdir, path).encode('utf-8')
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        if isinstance(content, list):
            os.mkdir(path)
        elif isinstance(content, str) and content.startswith('symlink://'):
            os.symlink(content[10:], path)
        else:
            mode = 'wb' if isinstance(content, bytes) else 'w'
            with open(path, mode) as f:
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
