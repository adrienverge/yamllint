# -*- coding: utf-8 -*-
import unittest
import string

from yamllint.format import escape_xml, severity_from_level


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
