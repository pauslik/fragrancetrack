from src.database import Database
from src.fragrance import Fragrance

def main():
    review_db = Database("review_db.json")
    print(review_db.df)
    lmlp = Fragrance("Jean Paul Gaultier", "Le Male Le Parfum", 10)
    vrse = Fragrance("Viktor & Rolf", "Spicebomb Extreme", 10)
    review_db.add_fragrance(lmlp)
    review_db.add_fragrance(vrse)
    print(review_db.df)
    review_db.remove_fragrance(vrse)
    print(review_db.df)


if __name__ == "__main__":
    main()
