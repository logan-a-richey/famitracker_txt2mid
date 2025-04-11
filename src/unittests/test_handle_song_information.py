#!/usr/bin/env python3

# NOTE
# src_dir = pwd at src/ level
# run `export PYTHONPATH=<src_dir>`
# check with `echo $PYTHONPATH`
# python3 -m unittest <name_of_test_file_without_extension> <(optional) name_of_test_function>
# if all goes well, all tests will pass!

import unittest
import sys
sys.dont_write_bytecode = True

from dummy_project import DummyProject
from stages.reader_handlers.handle_song_information import HandleSongInformation

class TestHandleSongInformation(unittest.TestCase):
    def setUp(self):
        self.project = DummyProject()
        self.handler = HandleSongInformation(self.project)

    # ---- Test Title Regex ---
    def test_title_1(self):
        self.assertTrue(self.handler.handle("TITLE \"my title\""))
    
    def test_title_2(self):
        self.assertTrue(self.handler.handle("TITLE \"my \"inner quote\" title\" # COMMENT"))
    
    def test_title_3(self):
        self.assertTrue(self.handler.handle("TITLE \"\""))
    
    def test_title_4(self):
        self.assertFalse(self.handler.handle("TITLE NAN"))

    # ---- Test Author Regex ---
    def test_author_1(self):
        self.assertTrue(self.handler.handle("AUTHOR \"my author\""))

    def test_author_2(self):
        self.assertTrue(self.handler.handle("AUTHOR \"my \"inner quote\" author\""))

    def test_author_3(self):
        self.assertTrue(self.handler.handle("AUTHOR \"\""))

    def test_author_4(self):
        self.assertFalse(self.handler.handle("AUTHOR NAN"))

    # ---- Test Copyright Regex ---
    def test_copyright_1(self):
        self.assertTrue(self.handler.handle("COPYRIGHT \"2025 (c)\""))

    def test_copyright_2(self):
        self.assertTrue(self.handler.handle("COPYRIGHT \"2025 \"inner quote\" (c)\""))

    def test_copyright_3(self):
        self.assertTrue(self.handler.handle("COPYRIGHT \"\""))

    def test_copyright_4(self):
        self.assertFalse(self.handler.handle("COPYRIGHT NAN"))
        
    # ---- Test Comment Regex ---
    def test_comment_1(self):
        self.assertTrue(self.handler.handle("COMMENT \"some comment\""))

    def test_comment_2(self):
        self.assertTrue(self.handler.handle("COMMENT \"some \"inner quote\" comment\""))

    def test_comment_3(self):
        self.assertTrue(self.handler.handle("COMMENT \"\""))

    def test_comment_4(self):
        self.assertFalse(self.handler.handle("COMMENT NAN"))


def main():
    unittest.main()


if __name__ == "__main__":
    main()

