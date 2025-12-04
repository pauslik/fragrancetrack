import os
import polars as pl
from fragrance import Fragrance

frag = Fragrance("Azzaro", "The Most Wanted Intense", 8, "Somehow they have EDP and EDT Intense versions")

# print(frag.__dict__)

df = pl.DataFrame(frag.__dict__)

# print(df)

df.write_json(os.path.abspath("./db/db.json"))

# df2 = pl.read_csv()