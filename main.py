import os
from src.database import Tracker
from src.fragrance import Fragrance

def main():
    tracker_db = Tracker("tracker_db.json")
    # tracker_db.import_db_from_excel(os.path.abspath("input/db/old.xlsx"))
    # tracker_db.import_db_from_excel(os.path.abspath("input/db/new.xlsx"))
    
    # leparfum = Fragrance("Jean Paul Gaultier", "Le Male Le Parfum")
    # tracker_db.update_fragrance(leparfum)

    reflection = Fragrance("Amouage", "Reflection Man")
    tracker_db.update_fragrance(reflection)

    print(tracker_db.df)


if __name__ == "__main__":
    main()
