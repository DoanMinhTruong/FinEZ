import pymongo
from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


client = MongoClient(host=os.environ.get("MONGO_HOST"),
                     port=int(os.environ.get("MONGO_PORT")), 
                     username=os.environ.get("MONGO_USERNAME"),
                     password=os.environ.get("MONGO_PASSWORD"),
                     authSource=os.environ.get("MONGO_USERNAME"))
db = client[os.environ.get("MONGO_DB")]
cols = db.list_collection_names()
res = []
for col in cols:
    for document in db[col].find():
        res.append(document)
        print(document)

ma = {}
for i in res:
    if(i['code'] not in ma):
        ma[i['code']] = 1
    else:
        ma[i['code']]+=1

print(ma)
