import unittest

from src.main import copy_files


class TestMain(unittest.TestCase):
    def test_copy_files(self):
        copy_files("./static","./docs")
