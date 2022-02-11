# -*- coding: utf-8 -*-
# flake8: noqa
import unittest
import string
import ddt

from yamllint.linter import LintProblem
from yamllint.format import (
    escape_xml,
    severity_from_level,
    Formater,
    ParsableFormater,
    GithubFormater,
    ColoredFormater,
    StandardFormater,
    JSONFormater,
    JunitFormater,
    CodeclimateFormater
)


class TextToXMLTestCase(unittest.TestCase):

    specials = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;'
    }

    def test_letters_chars(self):
        txt = string.ascii_letters
        self.assertEqual(escape_xml(txt), txt)

    def test_specials_chars(self):
        for inp, out in self.specials.items():
            self.assertEqual(escape_xml(inp), out)


class CodeClimateSeverityTestCase(unittest.TestCase):

    expected = {
        None: "info",
        'warning': "minor",
        'error': "major",
        0: "info",
        1: "minor",
        2: "major",
    }

    def test_specials_chars(self):
        for inp, out in self.expected.items():
            self.assertEqual(severity_from_level(inp), out)


class FormaterTestCase(unittest.TestCase):

    sublcasses = {
        "parsable": ParsableFormater,
        "github": GithubFormater,
        "colored": ColoredFormater,
        "standard": StandardFormater,
        "json": JSONFormater,
        "junitxml": JunitFormater,
        "codeclimate": CodeclimateFormater
    }

    def test_get_formaters_names(self):
        self.assertEqual(
            set(Formater.get_formaters_names()),
            set(self.sublcasses.keys())
        )

    def test_get_formater(self):
        for no_warn in [True, False]:
            for name, cls in self.sublcasses.items():
                res = Formater.get_formater(name, no_warn)
                self.assertTrue(isinstance(res, cls))
                self.assertEqual(res.no_warn, no_warn)

    def test_unknown_formater(self):
        with self.assertRaises(ValueError):
            Formater.get_formater("unknown", False)

    def test_abstract_class(self):
        inst = Formater(False)
        with self.assertRaises(NotImplementedError):
            inst.show_problems_for_all_files([])
        with self.assertRaises(NotImplementedError):
            inst.show_problems_for_file([], "a")
        with self.assertRaises(NotImplementedError):
            inst.show_problem(None, "a")


NONE = {}
NO_ERROR = {"file1.yml": []}
ONE_NOTHING = {"file1.yml": [
    LintProblem(1, 1, desc="desc of None", rule="my-rule")
]}
ONE_ERROR = {"file1.yml": [
    LintProblem(
        line=1,
        column=2,
        desc="desc of error",
        rule="my-rule",
        level="error"
    )
]}
ONE_WARNING = {"file1.yml": [
    LintProblem(
        line=1,
        column=2,
        desc="desc of warn",
        rule="my-rule",
        level="warning"
    )
]}
MIXED_ONE_FILE = {"file1.yml": [
    ONE_NOTHING["file1.yml"][0],
    ONE_ERROR["file1.yml"][0],
    ONE_WARNING["file1.yml"][0]
]}
MIXED_MULT_FILE = {
    "file1.yml": ONE_NOTHING["file1.yml"],
    "file2.yml": ONE_ERROR["file1.yml"],
    "file3.yml": ONE_WARNING["file1.yml"]
}


@ddt.ddt
class FormatersTestCase(unittest.TestCase):

    @ddt.data(
        # No errors
        (ParsableFormater(True), NONE, ""),
        (GithubFormater(True), NONE, ""),
        (ColoredFormater(True), NONE, ""),
        (StandardFormater(True), NONE, ""),
        (JSONFormater(True), NONE, "[]\n"),
        (CodeclimateFormater(True), NONE, "[]\n"),
        (ParsableFormater(True), NO_ERROR, ""),
        (GithubFormater(True), NO_ERROR, ""),
        (ColoredFormater(True), NO_ERROR, ""),
        (StandardFormater(True), NO_ERROR, ""),
        (JSONFormater(True), NO_ERROR, "[]\n"),
        (CodeclimateFormater(True), NO_ERROR, "[]\n"),
        (ParsableFormater(True), ONE_NOTHING, ""),
        (GithubFormater(True), ONE_NOTHING, ""),
        (ColoredFormater(True), ONE_NOTHING, ""),
        (StandardFormater(True), ONE_NOTHING, ""),
        (JSONFormater(True), ONE_NOTHING, '[]\n'),
        (CodeclimateFormater(True), ONE_NOTHING, '[]\n'),
        # Errors with no level are ignored
        (ParsableFormater(False), ONE_NOTHING, ""),
        (GithubFormater(False), ONE_NOTHING, ""),
        (ColoredFormater(False), ONE_NOTHING, ""),
        (StandardFormater(False), ONE_NOTHING, ""),
        (JSONFormater(False), ONE_NOTHING, '[]\n'),
        (CodeclimateFormater(False), ONE_NOTHING, '[]\n'),
        # 1 Skipped warning
        (ParsableFormater(True), ONE_WARNING, ""),
        (GithubFormater(True), ONE_WARNING, ""),
        (ColoredFormater(True), ONE_WARNING, ""),
        (StandardFormater(True), ONE_WARNING, ""),
        (JSONFormater(True), ONE_WARNING, '[]\n'),
        (CodeclimateFormater(True), ONE_WARNING, '[]\n'),
        # 1 Unskipped warning
        (ParsableFormater(False), ONE_WARNING, 'file1.yml:1:2: [warning] desc of warn (my-rule)\n'),
        (GithubFormater(False), ONE_WARNING, '::group::file1.yml\n::warning file=file1.yml,line=1,col=2::1:2 [my-rule] desc of warn\n::endgroup::\n\n'),
        (ColoredFormater(False), ONE_WARNING, '\x1b[4mfile1.yml\x1b[0m\n  \x1b[2m1:2\x1b[0m       \x1b[33mwarning\x1b[0m  desc of warn  \x1b[2m(my-rule)\x1b[0m\n\n'),
        (StandardFormater(False), ONE_WARNING, 'file1.yml\n  1:2       warning  desc of warn  (my-rule)\n\n'),
        (JSONFormater(False), ONE_WARNING, '[\n    {\n        "line": 1,\n        "column": 2,\n        "rule": "my-rule",\n        "level": "warning",\n        "message": "desc of warn",\n        "path": "file1.yml"\n    }\n]\n'),
        (CodeclimateFormater(False), ONE_WARNING, '[\n    {\n        "type": "issue",\n        "check_name": "my-rule",\n        "description": "desc of warn",\n        "content": "desc of warn (my-rule)",\n        "categories": [\n            "Style"\n        ],\n        "location": {\n            "path": "file1.yml",\n            "positions": {\n                "begin": {\n                    "line": 1,\n                    "column": 2\n                }\n            }\n        },\n        "remediation_points": 1000,\n        "severity": "minor"\n    }\n]\n'),
        # 1 Error
        (ParsableFormater(True), ONE_ERROR, 'file1.yml:1:2: [error] desc of error (my-rule)\n'),
        (GithubFormater(True), ONE_ERROR, '::group::file1.yml\n::error file=file1.yml,line=1,col=2::1:2 [my-rule] desc of error\n::endgroup::\n\n'),
        (ColoredFormater(True), ONE_ERROR, '\x1b[4mfile1.yml\x1b[0m\n  \x1b[2m1:2\x1b[0m       \x1b[31merror\x1b[0m    desc of error  \x1b[2m(my-rule)\x1b[0m\n\n'),
        (StandardFormater(True), ONE_ERROR, 'file1.yml\n  1:2       error    desc of error  (my-rule)\n\n'),
        (JSONFormater(True), ONE_ERROR, '[\n    {\n        "line": 1,\n        "column": 2,\n        "rule": "my-rule",\n        "level": "error",\n        "message": "desc of error",\n        "path": "file1.yml"\n    }\n]\n'),
        (CodeclimateFormater(True), ONE_ERROR, '[\n    {\n        "type": "issue",\n        "check_name": "my-rule",\n        "description": "desc of error",\n        "content": "desc of error (my-rule)",\n        "categories": [\n            "Style"\n        ],\n        "location": {\n            "path": "file1.yml",\n            "positions": {\n                "begin": {\n                    "line": 1,\n                    "column": 2\n                }\n            }\n        },\n        "remediation_points": 1000,\n        "severity": "major"\n    }\n]\n'),
        # mixed warn / err on the same file
        (ParsableFormater(False), MIXED_ONE_FILE, 'file1.yml:1:2: [error] desc of error (my-rule)\nfile1.yml:1:2: [warning] desc of warn (my-rule)\n'),
        (GithubFormater(False), MIXED_ONE_FILE, '::group::file1.yml\n::error file=file1.yml,line=1,col=2::1:2 [my-rule] desc of error\n::warning file=file1.yml,line=1,col=2::1:2 [my-rule] desc of warn\n::endgroup::\n\n'),
        (ColoredFormater(False), MIXED_ONE_FILE, '\x1b[4mfile1.yml\x1b[0m\n  \x1b[2m1:2\x1b[0m       \x1b[31merror\x1b[0m    desc of error  \x1b[2m(my-rule)\x1b[0m\n  \x1b[2m1:2\x1b[0m       \x1b[33mwarning\x1b[0m  desc of warn  \x1b[2m(my-rule)\x1b[0m\n\n'),
        (StandardFormater(False), MIXED_ONE_FILE, 'file1.yml\n  1:2       error    desc of error  (my-rule)\n  1:2       warning  desc of warn  (my-rule)\n\n'),
        (JSONFormater(False), MIXED_ONE_FILE, '[\n    {\n        "line": 1,\n        "column": 2,\n        "rule": "my-rule",\n        "level": "error",\n        "message": "desc of error",\n        "path": "file1.yml"\n    },\n    {\n        "line": 1,\n        "column": 2,\n        "rule": "my-rule",\n        "level": "warning",\n        "message": "desc of warn",\n        "path": "file1.yml"\n    }\n]\n'),
        (CodeclimateFormater(False), MIXED_ONE_FILE, '[\n    {\n        "type": "issue",\n        "check_name": "my-rule",\n        "description": "desc of error",\n        "content": "desc of error (my-rule)",\n        "categories": [\n            "Style"\n        ],\n        "location": {\n            "path": "file1.yml",\n            "positions": {\n                "begin": {\n                    "line": 1,\n                    "column": 2\n                }\n            }\n        },\n        "remediation_points": 1000,\n        "severity": "major"\n    },\n    {\n        "type": "issue",\n        "check_name": "my-rule",\n        "description": "desc of warn",\n        "content": "desc of warn (my-rule)",\n        "categories": [\n            "Style"\n        ],\n        "location": {\n            "path": "file1.yml",\n            "positions": {\n                "begin": {\n                    "line": 1,\n                    "column": 2\n                }\n            }\n        },\n        "remediation_points": 1000,\n        "severity": "minor"\n    }\n]\n'),
        # mixed warn / err on multiples files
        (ParsableFormater(False), MIXED_MULT_FILE, 'file2.yml:1:2: [error] desc of error (my-rule)\nfile3.yml:1:2: [warning] desc of warn (my-rule)\n'),
        (GithubFormater(False), MIXED_MULT_FILE, '::group::file2.yml\n::error file=file2.yml,line=1,col=2::1:2 [my-rule] desc of error\n::endgroup::\n\n::group::file3.yml\n::warning file=file3.yml,line=1,col=2::1:2 [my-rule] desc of warn\n::endgroup::\n\n'),
        (ColoredFormater(False), MIXED_MULT_FILE, '\x1b[4mfile2.yml\x1b[0m\n  \x1b[2m1:2\x1b[0m       \x1b[31merror\x1b[0m    desc of error  \x1b[2m(my-rule)\x1b[0m\n\n\x1b[4mfile3.yml\x1b[0m\n  \x1b[2m1:2\x1b[0m       \x1b[33mwarning\x1b[0m  desc of warn  \x1b[2m(my-rule)\x1b[0m\n\n'),
        (StandardFormater(False), MIXED_MULT_FILE, 'file2.yml\n  1:2       error    desc of error  (my-rule)\n\nfile3.yml\n  1:2       warning  desc of warn  (my-rule)\n\n'),
        (JSONFormater(False), MIXED_MULT_FILE, '[\n    {\n        "line": 1,\n        "column": 2,\n        "rule": "my-rule",\n        "level": "error",\n        "message": "desc of error",\n        "path": "file2.yml"\n    },\n    {\n        "line": 1,\n        "column": 2,\n        "rule": "my-rule",\n        "level": "warning",\n        "message": "desc of warn",\n        "path": "file3.yml"\n    }\n]\n'),
        (CodeclimateFormater(False), MIXED_MULT_FILE, '[\n    {\n        "type": "issue",\n        "check_name": "my-rule",\n        "description": "desc of error",\n        "content": "desc of error (my-rule)",\n        "categories": [\n            "Style"\n        ],\n        "location": {\n            "path": "file2.yml",\n            "positions": {\n                "begin": {\n                    "line": 1,\n                    "column": 2\n                }\n            }\n        },\n        "remediation_points": 1000,\n        "severity": "major"\n    },\n    {\n        "type": "issue",\n        "check_name": "my-rule",\n        "description": "desc of warn",\n        "content": "desc of warn (my-rule)",\n        "categories": [\n            "Style"\n        ],\n        "location": {\n            "path": "file3.yml",\n            "positions": {\n                "begin": {\n                    "line": 1,\n                    "column": 2\n                }\n            }\n        },\n        "remediation_points": 1000,\n        "severity": "minor"\n    }\n]\n'),
    )
    @ddt.unpack
    def test_all_formaters(self, inst, inp, ret):
        self.assertEqual(
            inst.show_problems_for_all_files(inp),
            ret
        )