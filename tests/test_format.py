# -*- coding: utf-8 -*-
import unittest
import string

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


class FormatersTestCase(unittest.TestCase):

    args = [
        (ParsableFormater(True), {"file1.yml": []}, ""),
    ]

    def test_all_formaters(self):
        for inst, inp, ret in self.args:
            self.assertEqual(
                inst.show_problems_for_all_files(inp),
                ret
            )
