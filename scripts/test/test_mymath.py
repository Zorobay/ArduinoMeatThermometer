import unittest

from scripts.lib import mymath


class TestMyMath(unittest.TestCase):
    
    def test_root_negative(self):
        self.assertEqual(mymath.root(-4), -2)
        self.assertEqual(mymath.root(4), 2)