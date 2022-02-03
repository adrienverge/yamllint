
from __future__ import print_function

import os
import platform
import sys

from yamllint.linter import PROBLEM_LEVELS


def supports_color():
    supported_platform = not (platform.system() == 'Windows' and not
                              ('ANSICON' in os.environ or
                               ('TERM' in os.environ and
                                os.environ['TERM'] == 'ANSI')))
    return (supported_platform and
            hasattr(sys.stdout, 'isatty') and sys.stdout.isatty())


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
        line = '  %d:%d' % (problem.line, problem.column)
        line += max(12 - len(line), 0) * ' '
        line += problem.level
        line += max(21 - len(line), 0) * ' '
        line += problem.desc
        if problem.rule:
            line += '  (%s)' % problem.rule
        return line

    @staticmethod
    def standard_color(problem, filename):
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

    @staticmethod
    def github(problem, filename):
        line = '::'
        line += problem.level
        line += ' file=' + filename + ','
        line += 'line=' + format(problem.line) + ','
        line += 'col=' + format(problem.column)
        line += '::'
        line += format(problem.line)
        line += ':'
        line += format(problem.column)
        line += ' '
        if problem.rule:
            line += '[' + problem.rule + '] '
        line += problem.desc
        return line


def show_problems(problems, file, args_format, no_warn):
    max_level = 0
    first = True

    if args_format == 'auto':
        if ('GITHUB_ACTIONS' in os.environ and
                'GITHUB_WORKFLOW' in os.environ):
            args_format = 'github'
        elif supports_color():
            args_format = 'colored'

    for problem in problems:
        max_level = max(max_level, PROBLEM_LEVELS[problem.level])
        if no_warn and (problem.level != 'error'):
            continue
        if args_format == 'parsable':
            print(Format.parsable(problem, file))
        elif args_format == 'github':
            if first:
                print('::group::%s' % file)
                first = False
            print(Format.github(problem, file))
        elif args_format == 'colored':
            if first:
                print('\033[4m%s\033[0m' % file)
                first = False
            print(Format.standard_color(problem, file))
        else:
            if first:
                print(file)
                first = False
            print(Format.standard(problem, file))

    if not first and args_format == 'github':
        print('::endgroup::')

    if not first and args_format != 'parsable':
        print('')

    return max_level


def show_all_problems(all_problems, args_format, no_warn):
    """Print all problems, return the max level."""
    max_level = 0

    for file, problem in all_problems.items():
        curr_level = show_problems(problem, file, args_format, no_warn)
        max_level = max(curr_level, max_level)

    return max_level
