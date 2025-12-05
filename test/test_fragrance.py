import unittest

from src.fragrance import Fragrance

class TestFragrance(unittest.TestCase):
    def test_special_methods(self):
        # init
        frag1 = Fragrance("Azzaro", "The Most Wanted Intense")
        frag2 = Fragrance("Azzaro", "The Most Wanted Parfum", 10)
        frag3 = Fragrance("Azzaro", "The Most Wanted Intense", 8)
        # repr
        string1 = str(frag1)
        string2 = str(frag2)
        self.assertEqual(string1, "Azzaro - The Most Wanted Intense")
        self.assertEqual(string2, "Azzaro - The Most Wanted Parfum (10)")
        # eq
        self.assertEqual(frag1, frag3)
        self.assertNotEqual(frag1, frag2)

if __name__ == "__main__":
    unittest.main()