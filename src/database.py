import os
import polars as pl
# from src.fragrance import Fragrance

TRACK_DB = "db.json"

def load_db(path):
    if (os.path.exists(path)):
        df = pl.read_json(path)
    else:
        df = pl.DataFrame({})
    return df


class Database():
    def __init__(self) -> None:
        self.dir = os.path.abspath("./db")
        self.df = load_db(os.path.join(self.dir, TRACK_DB))