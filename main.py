import os
from src.database import Tracker
from src.fragrance import Fragrance

def main():
    tracker_db = Tracker("tracker_db.json")
    
    tracker_db.check_all_cards()

    tracker_db._save_db(overwrite=True)


if __name__ == "__main__":
    main()
