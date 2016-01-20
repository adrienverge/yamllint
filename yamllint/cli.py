#!/usr/bin/env python
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

from __future__ import print_function
import os.path
import sys

import argparse

from yamllint import APP_DESCRIPTION, APP_NAME, APP_VERSION
from yamllint import config
from yamllint.errors import YamlLintConfigError
from yamllint import lint


class Format(object):
    @staticmethod
    def parsable(problem, filename):
        return ('%(file)s:%(line)s:%(column)s: [%(level)s] %(message)s' %
                {'file': filename,
                 'line': problem.line,
                 'column': problem.column,
                 'level': problem.level,
                 'message': problem.message})

    @staticmethod
    def standard(problem, filename):
        line = '  \033[2m%d:%d\033[0m' % (problem.line, problem.column)
        line += max(20 - len(line), 0) * ' '
        if problem.level == 'warning':
            line += '\033[33m%s\033[0m' % problem.level
        else:
            line += '\033[31m%s\033[0m' % problem.level
        line += max(38 - len(line), 0) * ' '
        line += problem.desc
        if problem.rule:
            line += '  \033[2m(%s)\033[0m' % problem.rule
        return line


def run(argv):
    parser = argparse.ArgumentParser(prog=APP_NAME,
                                     description=APP_DESCRIPTION)
    parser.add_argument('files', metavar='FILES', nargs='+',
                        help='files to check')
    parser.add_argument('-c', '--config', dest='config_file', action='store',
                        help='path to a custom configuration')
    parser.add_argument('-f', '--format',
                        choices=('parsable', 'standard'), default='standard',
                        help='format for parsing output')
    parser.add_argument('-v', '--version', action='version',
                        version='%s %s' % (APP_NAME, APP_VERSION))

    # TODO: read from stdin when no filename?

    args = parser.parse_args(argv)

    try:
        if args.config_file is not None:
            conf = config.parse_config_from_file(args.config_file)
        elif os.path.isfile('.yamllint'):
            conf = config.parse_config_from_file('.yamllint')
        else:
            conf = config.parse_config('extends: default')
    except YamlLintConfigError as e:
        print(e, file=sys.stderr)
        sys.exit(-1)

    return_code = 0

    for file in args.files:
        if args.format != 'parsable':
            print('\033[4m%s\033[0m' % file)

        try:
            with open(file) as f:
                for problem in lint(f, conf):
                    if args.format == 'parsable':
                        print(Format.parsable(problem, file))
                    else:
                        print(Format.standard(problem, file))

                    if return_code == 0 and problem.level == 'error':
                        return_code = 1
        except EnvironmentError as e:
            print(e)
            return_code = -1

        if args.format != 'parsable':
            print('')

    sys.exit(return_code)
