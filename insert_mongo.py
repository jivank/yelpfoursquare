from pymongo import MongoClient
import json


def make_connection():
    client = MongoClient('localhost', 27017)
    db = client.testdb
    businesses = db.businesscollection
    return (client, businesses)


def final_json_to_mongo():
    c, b = make_connection()
    for x in json.loads(open('final.json').read()):
        b.insert_one(x)
