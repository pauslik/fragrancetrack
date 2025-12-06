import os
import polars as pl
from src.fragrance import Fragrance

class Database():
    def __init__(self, file, schema: pl.Schema) -> None:
        # db file
        self.dir = os.path.abspath("./db")
        self.file = file
        self.path = os.path.join(self.dir, self.file)
        # Must be implemented by subclass
        self.schema = schema
        # try loading existing database, create new otherwise
        self.df = self._load_db()

    def import_db_from_excel(self, filepath):
        import_df = pl.read_excel(filepath)
        # raises exceptions if schema is not correct
        schema_check = self.df.match_to_schema(import_df.collect_schema(), extra_columns='ignore')
        new_df = self.df.vstack(import_df)
        self.df = new_df
        self._save_db(overwrite=True)


    def save_copy(self, filepath):
        if os.path.exists(filepath):
            raise Exception(f'File already exists: {filepath}')
        else:
            self.df.write_json(filepath)
        return True
    
    # DB load/save
    def _load_db(self):
        if (os.path.exists(self.path)):
            df = pl.read_json(self.path)
            if not df.is_empty():
                return df
        # runs if file doesn't exist or is empty
        df = self.schema.to_frame()
        return df
    
    def _save_db(self, overwrite = False):
        if not overwrite and os.path.exists(self.path):
            raise Exception("Database already exists. Use 'force' option to overwrite.")
        else:
            self.df.write_json(self.path)
        return True


class Public(Database):
    def __init__(self, file) -> None:
        self.schema = pl.Schema({"brand": pl.String(), "name": pl.String()})
        super().__init__(file=file, schema=self.schema)


class Tracker(Database):
    def __init__(self, file) -> None:
        # db schema: MUST MATCH FRAGRANCE CLASS FIELDS
        # TODO make a schema builder from class variables
        self.schema = pl.Schema({"brand": pl.String(), "name": pl.String(), "my_score": pl.Int64()})
        super().__init__(file=file, schema=self.schema)  

    def get_fragrance(self, brand, name) -> Fragrance:
        frag = Fragrance(brand, name)
        condition = self._condition(frag)
        if self._frag_exists(condition):
            df = self.df.filter(condition)
            df_dict = df.row(0, named=True)
            clean_dict = {k: v for k, v in df_dict.items() if v is not None}
            frag = Fragrance(**clean_dict)
        else:
            raise Exception(f'Fragrance not in database: {brand} - {name}')
        return frag

    def add_fragrance(self, frag: Fragrance):
        new_row = pl.DataFrame(frag.__dict__)
        if self._frag_exists(self._condition(frag)):
            # TODO if exists, call update for provided fields?
            return False
        else:
            self._add_inplace(new_row)
            return True

    def update_fragrance(self, frag: Fragrance):
        new_row = pl.DataFrame(frag.__dict__)
        if self._frag_exists(self._condition(frag)):
            self._update_inplace(new_row)
            return True
        else:
            self.add_fragrance(frag)
            return False

    def remove_fragrance(self, frag: Fragrance):
        # Need to get the Fragrance object from the existing Database in order to remove it
        condition = self._condition(frag)
        removed = self._remove_inplace(condition)
        return removed
        


    # DB manipulation helper methods
    def _condition(self, frag: Fragrance):
        brand = frag.brand
        name = frag.name
        return (pl.col("brand") == brand) & (pl.col("name") == name)

    def _frag_exists(self, condition) -> bool:
        exists = self.df.select(condition.any()).item()
        return exists

    def _add_inplace(self, new_row: pl.DataFrame):
        self.df = self.df.vstack(new_row)
        self._save_db(overwrite=True)
        return True
    
    def _update_inplace(self, new_row: pl.DataFrame):
        self.df = self.df.update(new_row)
        self._save_db(overwrite=True)
        return True
    
    def _remove_inplace(self, condition) -> pl.DataFrame:
        deleted = self.df.filter(condition)
        self.df = self.df.filter(~condition)
        self._save_db(overwrite=True)
        return deleted


