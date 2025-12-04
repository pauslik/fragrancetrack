import unittest

from src.fragrance import Fragrance

class TestClassSpecialMethods(unittest.TestCase):
    def test_dunders(self):
        # init
        frag1 = Fragrance("Azzaro", "The Most Wanted Intense")
        frag2 = Fragrance("Azzaro", "The Most Wanted Parfum", 10, "Even stronger spices with vanilla.")
        frag3 = Fragrance("Azzaro", "The Most Wanted Intense", 8, "Somehow they have EDP and EDT Intense versions")
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