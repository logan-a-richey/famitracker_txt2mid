#!/usr/bin/env python3

# NOTE
# src_dir = pwd at src/ level
# run `export PYTHONPATH=<src_dir>`
# check with `echo $PYTHONPATH`
# python3 -m unittest <name_of_test_file_without_extension> <(optional) name_of_test_function>
# if all goes well, all tests will pass!

import unittest
from mock_handler import MockHandler
from utils.regex_patterns import RegexPatterns

class TestHandleSongInformation(unittest.TestCase):
    def setUp(self):
        self.handler = MockHandler()
        self.handler.pattern = RegexPatterns.patterns['song_information']

    # ---- Test Title Regex ---
    def test_title_1(self):
        self.assertEqual(self.handler.handle("TITLE \"my title\""), 0)
    
    def test_title_2(self):
        self.assertEqual(self.handler.handle("TITLE \"my \"inner quote\" title\" # COMMENT"), 0)
    
    def test_title_3(self):
        self.assertEqual(self.handler.handle("TITLE \"\""), 0)
    
    def test_title_4(self):
        self.assertNotEqual(self.handler.handle("TITLE NAN"), 0)

    # ---- Test Author Regex ---
    def test_author_1(self):
        self.assertEqual(self.handler.handle("AUTHOR \"my author\""), 0)

    def test_author_2(self):
        self.assertEqual(self.handler.handle("AUTHOR \"my \"inner quote\" author\""), 0)

    def test_author_3(self):
        self.assertEqual(self.handler.handle("AUTHOR \"\""), 0)

    def test_author_4(self):
        self.assertNotEqual(self.handler.handle("AUTHOR NAN"), 0)

    # ---- Test Copyright Regex ---
    def test_copyright_1(self):
        self.assertEqual(self.handler.handle("COPYRIGHT \"2025 (c)\""), 0)

    def test_copyright_2(self):
        self.assertEqual(self.handler.handle("COPYRIGHT \"2025 \"inner quote\" (c)\""), 0)

    def test_copyright_3(self):
        self.assertEqual(self.handler.handle("COPYRIGHT \"\""), 0)

    def test_copyright_4(self):
        self.assertNotEqual(self.handler.handle("COPYRIGHT NAN"), 0)
        
    # ---- Test Comment Regex ---
    def test_comment_1(self):
        self.assertEqual(self.handler.handle("COMMENT \"some comment\""), 0)

    def test_comment_2(self):
        self.assertEqual(self.handler.handle("COMMENT \"some \"inner quote\" comment\""), 0)

    def test_comment_3(self):
        self.assertEqual(self.handler.handle("COMMENT \"\""), 0)

    def test_comment_4(self):
        self.assertNotEqual(self.handler.handle("COMMENT NAN"), 0)


def main():
    unittest.main()


if __name__ == "__main__":
    main()

