import unittest
import os, sys
import polars as pl

from cleanup import TempFiles
from src.fragrance import Fragrance
from src.database import Database
from polars.testing import assert_frame_equal, assert_frame_not_equal

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_files = TempFiles()
    
    def tearDown(self):
        self.temp_files.cleanup()

    def test_read_write(self):
        # create
        frag1 = Fragrance("Azzaro", "The Most Wanted Intense")
        frag2 = Fragrance("Azzaro", "The Most Wanted Parfum", 10, "Even stronger spices with vanilla.")
        frag3 = Fragrance("Azzaro", "The Most Wanted Intense", 8, "Somehow they have EDP and EDT Intense versions")
        df = pl.DataFrame([frag1.__dict__, frag2.__dict__, frag3.__dict__])
        # write
        db_file = os.path.abspath("./db/test_db.json")
        df.write_json(os.path.abspath(db_file))
        self.temp_files.add_file(db_file)
        # read
        db = Database("test_db.json")
        assert_frame_equal(df, db.df)


if __name__ == "__main__":
    unittest.main()