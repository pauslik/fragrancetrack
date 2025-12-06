import unittest
import os, sys
import polars as pl

from cleanup import TempFiles
from src.fragrance import Fragrance
from src.database import Tracker, PublicList
from polars.testing import assert_frame_equal, assert_frame_not_equal

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_files = TempFiles()
        # database file info, to be removed after tests
        cls.db_file = os.path.abspath("./db/test_db.json")
        cls.temp_files.add_file(cls.db_file)
        # database to be used in all tests
        cls.db = Tracker("test_db.json")

    @classmethod
    def tearDownClass(cls):
        cls.temp_files.cleanup()

    def test_read_write(self):
        # create
        frag1 = Fragrance("Jean Paul Gaultier", "Le Male Le Parfum", 10)
        frag2 = Fragrance("Viktor & Rolf", "Spicebomb Extreme")
        frag3 = Fragrance("Azzaro", "The Most Wanted Parfum", 10)
        frag4 = Fragrance("Azzaro", "The Most Wanted Intense", 8)
        df = pl.DataFrame([frag1.__dict__, frag2.__dict__, frag3.__dict__, frag4.__dict__])
        # write
        df.write_json(os.path.abspath(self.db_file))
        # read
        self.db = Tracker("test_db.json")
        assert_frame_equal(df, self.db.df)

    def test_add_frag(self):
        new_frag = Fragrance("Versace", "Eros", 10)
        # new
        self.assertTrue(self.db.add_fragrance(new_frag))
        # existing
        self.assertFalse(self.db.add_fragrance(new_frag))

    def test_get_frag(self):
        new_frag = Fragrance("Versace", "Eros EDP", 9)
        self.db.add_fragrance(new_frag)
        found = self.db.get_fragrance("Versace", "Eros EDP")
        self.assertTrue(new_frag, found)
        with self.assertRaises(Exception):
            self.db.get_fragrance("Versace", "Eros Flame")

    def test_remove_frag(self):
        frag1 = Fragrance("Jean Paul Gaultier", "Le Male Le Parfum", 10)
        frag2 = Fragrance("Viktor & Rolf", "Spicebomb Extreme")
        self.db.add_fragrance(frag1)
        self.db.add_fragrance(frag2)
        # .drop because of different column types
        df = pl.DataFrame(frag2.__dict__)
        df = df.drop(df.columns[2:])
        removed = self.db.remove_fragrance(frag2)
        removed = removed.drop(removed.columns[2:])
        assert_frame_equal(removed, df)

    def test_update_frag(self):
        frag1 = Fragrance("Kajal", "Aican")
        frag2 = Fragrance("Kajal", "Aican", 10)
        df1 = pl.DataFrame(frag1.__dict__)
        df2 = pl.DataFrame(frag2.__dict__)
        df1 = df1.drop(df1.columns[2:])
        df2 = df2.drop(df2.columns[2:])
        # not in DB
        self.assertFalse(self.db.update_fragrance(frag1))
        df1_db = pl.DataFrame(self.db.get_fragrance("Kajal", "Aican").__dict__)
        df1_db = df1_db.drop(df1_db.columns[2:])
        assert_frame_equal(df1_db, df1)
        self.assertTrue(self.db.update_fragrance(frag2))
        df2_db = pl.DataFrame(self.db.get_fragrance("Kajal", "Aican").__dict__)
        df2_db = df2_db.drop(df2_db.columns[2:])
        assert_frame_equal(df2_db, df2)
        


if __name__ == "__main__":
    unittest.main()