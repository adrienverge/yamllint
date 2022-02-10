# -*- coding: utf-8 -*-
import unittest
import string
import ddt

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
ONE_ERROR = {}
ONE_WARNING = {}


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
    )
    @ddt.unpack
    def test_all_formaters(self, inst, inp, ret):
        self.assertEqual(
            inst.show_problems_for_all_files(inp),
            ret
        )
