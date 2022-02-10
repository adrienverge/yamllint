# -*- coding: utf-8 -*-
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


@ddt.ddt
class FormatersTestCase(unittest.TestCase):

    @ddt.data(
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
        (ParsableFormater(True), ONE_WARNING, ""),
        (GithubFormater(True), ONE_WARNING, ""),
        (ColoredFormater(True), ONE_WARNING, ""),
        (StandardFormater(True), ONE_WARNING, ""),
        (JSONFormater(True), ONE_WARNING, '[\n    {\n        "line": 1,\n        "column": 2,\n        "rule": "my-rule",\n        "level": "warning",\n        "message": "desc of warn",\n        "path": "file1.yml"\n    }\n]\n'),
        (CodeclimateFormater(True), ONE_WARNING, '[\n    {\n        "type": "issue",\n        "check_name": "my-rule",\n        "description": "desc of warn",\n        "content": "desc of warn (my-rule)",\n        "categories": [\n            "Style"\n        ],\n        "location": {\n            "path": "file1.yml",\n            "positions": {\n                "begin": {\n                    "line": 1,\n                    "column": 2\n                }\n            }\n        },\n        "remediation_points": 1000,\n        "severity": "minor"\n    }\n]\n'),
        (ParsableFormater(True), ONE_ERROR, 'file1.yml:1:2: [error] desc of error (my-rule)\n'),
        (GithubFormater(True), ONE_ERROR, '::group::file1.yml\n::error file=file1.yml,line=1,col=2::1:2 [my-rule] desc of error\n::endgroup::\n\n'),
        (ColoredFormater(True), ONE_ERROR, '\x1b[4mfile1.yml\x1b[0m\n  \x1b[2m1:2\x1b[0m       \x1b[31merror\x1b[0m    desc of error  \x1b[2m(my-rule)\x1b[0m\n\n'),
        (StandardFormater(True), ONE_ERROR, 'file1.yml\n  1:2       error    desc of error  (my-rule)\n\n'),
        (JSONFormater(True), ONE_ERROR, '[\n    {\n        "line": 1,\n        "column": 2,\n        "rule": "my-rule",\n        "level": "error",\n        "message": "desc of error",\n        "path": "file1.yml"\n    }\n]\n'),
        (CodeclimateFormater(True), ONE_ERROR, '[\n    {\n        "type": "issue",\n        "check_name": "my-rule",\n        "description": "desc of error",\n        "content": "desc of error (my-rule)",\n        "categories": [\n            "Style"\n        ],\n        "location": {\n            "path": "file1.yml",\n            "positions": {\n                "begin": {\n                    "line": 1,\n                    "column": 2\n                }\n            }\n        },\n        "remediation_points": 1000,\n        "severity": "major"\n    }\n]\n'),
    )
    @ddt.unpack
    def test_all_formaters(self, inst, inp, ret):
        self.assertEqual(
            inst.show_problems_for_all_files(inp),
            ret
        )
