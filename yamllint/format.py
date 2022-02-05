
from __future__ import print_function

import os
import platform
import sys
import json
import datetime

from yamllint.linter import PROBLEM_LEVELS


def supports_color():
    supported_platform = not (platform.system() == 'Windows' and not
                              ('ANSICON' in os.environ or
                               ('TERM' in os.environ and
                                os.environ['TERM'] == 'ANSI')))
    return (supported_platform and
            hasattr(sys.stdout, 'isatty') and sys.stdout.isatty())


def run_on_gh():
    """Return if the currnet job is on github."""
    return 'GITHUB_ACTIONS' in os.environ and 'GITHUB_WORKFLOW' in os.environ


def escape_xml(text):
    """Escape text for XML."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace('"', '&apos;')
    return text


class Formater(object):
    """Any formater."""
    # the formater name
    name = ''

    @classmethod
    def get_formater(cls, name, no_warn):
        """Return a formater instance."""

        if name == 'auto':
            if run_on_gh():
                name = 'github'
            elif supports_color():
                name = 'colored'
            else:
                name = 'standard'

        for formater in cls.__subclasses__():
            if name == formater.name:
                return formater(no_warn)
        raise ValueError('unknown formater: %s' % name)

    def __init__(self, no_warn):
        """Setup the formater."""
        self.no_warn = no_warn

    def show_problems_for_all_files(self, all_problems):
        """Show all problems of all files."""
        raise NotImplementedError()

    def show_problems_for_file(self, problems, file):
        """Show all problems of a specific file."""
        raise NotImplementedError()

    def show_problem(self, problem, file):
        """Show all problems of a specific file."""
        raise NotImplementedError()


class ParsableFormater(Formater):
    """The parsable formater."""
    name = 'parsable'

    def show_problems_for_all_files(self, all_problems):
        """Show all problems of all files."""
        string = ''
        for file, problems in all_problems.items():
            string += self.show_problems_for_file(problems, file)
        return string

    def show_problems_for_file(self, problems, file):
        """Show all problems of a specific file."""
        string = ''
        for problem in problems:
            string += self.show_problem(problem, file)
        return string

    def show_problem(self, problem, file):
        """Show all problems of a specific file."""
        if self.no_warn and (problem.level != 'error'):
            return ''
        return (
            '%(file)s:%(line)s:%(column)s: [%(level)s] %(message)s\n' %
            {
                'file': file,
                'line': problem.line,
                'column': problem.column,
                'level': problem.level,
                'message': problem.message
            }
        )


class GithubFormater(Formater):
    """The parsable formater."""
    name = 'github'

    def show_problems_for_all_files(self, all_problems):
        """Show all problems of all files."""
        string = ''
        for file, problems in all_problems.items():
            string += self.show_problems_for_file(problems, file)
        return string

    def show_problems_for_file(self, problems, file):
        """Show all problems of a specific file."""
        string = '::group::%s\n' % file
        for problem in problems:
            string += self.show_problem(problem, file)
        if string == '::group::%s\n' % file:
            return ''
        return string + '::endgroup::\n\n'

    def show_problem(self, problem, file):
        """Show all problems of a specific file."""
        if self.no_warn and (problem.level != 'error'):
            return ''
        line = '::'
        line += problem.level
        line += ' file=' + file + ','
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
        line += '\n'
        return line


class ColoredFormater(Formater):
    """The parsable formater."""
    name = 'colored'

    def show_problems_for_all_files(self, all_problems):
        """Show all problems of all files."""
        string = ''
        for file, problems in all_problems.items():
            string += self.show_problems_for_file(problems, file)
        return string

    def show_problems_for_file(self, problems, file):
        """Show all problems of a specific file."""
        string = '\033[4m%s\033[0m\n' % file
        for problem in problems:
            string += self.show_problem(problem, file)
        if string == '\033[4m%s\033[0m\n' % file:
            return ''
        return string + '\n'

    def show_problem(self, problem, file):
        """Show all problems of a specific file."""
        if self.no_warn and (problem.level != 'error'):
            return ''
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
        line += '\n'
        return line


class StandardFormater(Formater):
    """The parsable formater."""
    name = 'standard'

    def show_problems_for_all_files(self, all_problems):
        """Show all problems of all files."""
        string = ''
        for file, problems in all_problems.items():
            string += self.show_problems_for_file(problems, file)
        return string

    def show_problems_for_file(self, problems, file):
        """Show all problems of a specific file."""
        string = file + '\n'
        for problem in problems:
            string += self.show_problem(problem, file)
        if string == file + '\n':
            return ''
        return string + '\n'

    def show_problem(self, problem, file):
        """Show all problems of a specific file."""
        if self.no_warn and (problem.level != 'error'):
            return ''
        line = '  %d:%d' % (problem.line, problem.column)
        line += max(12 - len(line), 0) * ' '
        line += problem.level
        line += max(21 - len(line), 0) * ' '
        line += problem.desc
        if problem.rule:
            line += '  (%s)' % problem.rule
        line += '\n'
        return line


class JSONFormater(Formater):
    """The parsable formater."""
    name = 'json'

    def show_problems_for_all_files(self, all_problems):
        """Show all problems of all files."""
        lst = []
        for k, v in all_problems.items():
            lst += self.show_problems_for_file(v, k)
        return json.dumps(lst, indent=4) + '\n'

    def show_problems_for_file(self, problems, file):
        """Show all problems of a specific file."""
        return list(map(self.show_problem, problems, [file] * len(problems)))

    def show_problem(self, problem, file):
        """Show all problems of a specific file."""
        return {**problem.dict, "path": file}


class JunitFormater(Formater):
    """The parsable formater."""
    name = 'junitxml'

    def show_problems_for_all_files(self, all_problems):
        """Show all problems of all files."""
        string = '<?xml version="1.0" encoding="utf-8"?>\n<testsuites>\n'

        errors = warnings = 0
        lst = []
        for k, v in all_problems.items():
            lst += self.show_problems_for_file(v, k)

        lines = []
        for item in lst:
            if item['level'] is None:
                continue
            elif item['level'] == 'warning':
                warnings += 1
                to_append = '<testcase classname="%s:%d:%d" name="%s" time="0.0"><failure message="%s"><\/failure><\/testcase>'  # noqa
            elif item['level'] == 'error':
                errors += 1
                to_append = '<testcase classname="%s:%d:%d" name="%s" time="0.0"><error message="%s"><\/error><\/testcase>'  # noqa
            lines.append(' ' * 8 + to_append % (
                item['file'],
                item['line'],
                item['column'],
                item['rule'],
                escape_xml(item['desc']))
            )

        string += ' '*4 + '<testsuite name="pytest" errors="%d" failures="%d" skipped="0" tests="%d" time="0" timestamp="%s" hostname="%s">\n' % (errors, warnings, errors + warnings, datetime.datetime.now().isoformat(), platform.node())  # noqa
        string += '\n'.join(lines) + '\n'
        string += '    </testsuite>\n</testsuites>\n'
        return string

    def show_problems_for_file(self, problems, file):
        """Show all problems of a specific file."""
        return list(map(self.show_problem, problems, [file] * len(problems)))

    def show_problem(self, problem, file):
        """Show all problems of a specific file."""
        return {**problem.dict, "file": file}


def max_level(all_problems):
    """Return the max level of all problems."""
    all_levels = [problem.level for problems in all_problems.values() for problem in problems]
    if all_levels:
        return max(map(lambda x: PROBLEM_LEVELS[x], all_levels))
    return 0


def show_all_problems(all_problems, args_format, no_warn):
    """Print all problems, return the max level."""

    fmt = Formater.get_formater(args_format, no_warn)

    print(fmt.show_problems_for_all_files(all_problems), end='')

    return max_level(all_problems)