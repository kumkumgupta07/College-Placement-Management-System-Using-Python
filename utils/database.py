# utils/database.py

from pymongo import MongoClient
from config import MONGO_URI

_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client["college_placement_db"]

def get_collection(name):
    return get_db()[name]
