import unittest
from LimbleConnection.util import collapse_redundant_path_parts

class TestNamingUtils(unittest.TestCase):
    def test_collapse_redundant_path_parts_identical(self):
        self.assertEqual(collapse_redundant_path_parts(['assets', 'assets']), ['assets'])
        self.assertEqual(collapse_redundant_path_parts(['locations', 'locations']), ['locations'])

    def test_collapse_redundant_path_parts_get_prefix(self):
        self.assertEqual(collapse_redundant_path_parts(['bills', 'get_bills']), ['bills'])
        self.assertEqual(collapse_redundant_path_parts(['teams', 'get_teams']), ['teams'])

    def test_collapse_redundant_path_parts_not_redundant(self):
        self.assertEqual(collapse_redundant_path_parts(['assets', 'fields']), ['assets', 'fields'])
        self.assertEqual(collapse_redundant_path_parts(['bills', 'create_bill']), ['bills', 'create_bill'])

    def test_collapse_redundant_path_parts_single(self):
        self.assertEqual(collapse_redundant_path_parts(['assets']), ['assets'])

    def test_collapse_redundant_path_parts_empty(self):
        self.assertEqual(collapse_redundant_path_parts([]), [])
