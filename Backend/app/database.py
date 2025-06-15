from pymongo import MongoClient
import os

def get_mongo_client():
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb+srv://user:password@cluster0.mongodb.net"))
    return client

def get_database(nameDB):
    client = get_mongo_client()
    db = client[nameDB]
    return db
