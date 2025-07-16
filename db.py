import configparser
import os
from pymongo import MongoClient


config_file = configparser.ConfigParser()
config_file.read(os.path.join(os.path.dirname(__file__), "bot.config"))

mongo_uri            = config_file.get("general","mongo_uri")
client               = MongoClient(MONGO_URI)
db                   = client["watch_price_bot"]
watchlist_collection = db["watchlist"]


def add_to_watchlist(user_id, item):
    user_id = str(user_id)
    existing = watchlist_collection.find_one({"user_id": user_id})
    if existing:
        watchlist_collection.update_one(
            {"user_id": user_id},
            {"$push": {"items": item}}
        )
    else:
        watchlist_collection.insert_one({
            "user_id": user_id,
            "items": [item]
        })


def get_watchlist(user_id):
    doc = watchlist_collection.find_one({"user_id": str(user_id)})
    return doc["items"] if doc else []


def remove_from_watchlist(user_id, index):
    doc = watchlist_collection.find_one({"user_id": str(user_id)})
    if not doc or index < 0 or index >= len(doc["items"]):
        return None

    item = doc["items"][index]
    watchlist_collection.update_one(
        {"user_id": str(user_id)},
        {"$pull": {"items": item}}
    )
    return item


def get_all_watch_entries():
    return list(watchlist_collection.find({}))