import pymongo

from DataBet.settings import DATABASE_HOST


def remove_data():
    MONGODB_URI = DATABASE_HOST
    # Connect to your MongoDB cluster:
    client = pymongo.MongoClient(MONGODB_URI)
    # Get a reference to the "sample_mflix" database:
    db = client["Bet"]
    # Get a reference to the "movies" collection:
    collection = db["crawler_match"]
    x = collection.delete_many({})
    print(x.deleted_count, ": deleted.")