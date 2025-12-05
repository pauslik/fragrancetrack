from src.database import Database

def main():
    review_db = Database("review_db.json")
    print(review_db.df)


if __name__ == "__main__":
    main()
