import os
import polars as pl
# from src.fragrance import Fragrance



class Database():
    def __init__(self, file) -> None:
        self.dir = os.path.abspath("./db")
        self.file = file
        self.df = self.load_db(os.path.join(self.dir, self.file))

    def load_db(self, path):
        if (os.path.exists(path)):
            df = pl.read_json(path)
        else:
            df = pl.DataFrame({})
        return df
    
    def save_db(self, df: pl.DataFrame, path, force = False):
        if not force and os.path.exists(path):
            raise Exception("Database already exists. Use 'force' option to overwrite.")
        else:
            df.write_json(path)
        return True