import os
from src.database import Database
from src.fragrance import Fragrance

def main():
    review_db = Database("review_db.json")
    # review_db.import_db_from_excel(os.path.abspath("input/old.xlsx"))
    # review_db.import_db_from_excel(os.path.abspath("input/new.xlsx"))
    print(review_db.df)


if __name__ == "__main__":
    main()
