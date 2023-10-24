from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


app = Flask(__name__)
client = MongoClient(host=os.environ.get("MONGO_HOST"),
                     port=int(os.environ.get("MONGO_PORT")), 
                     username=os.environ.get("MONGO_USERNAME"),
                     password=os.environ.get("MONGO_PASSWORD"),
                     authSource=os.environ.get("MONGO_USERNAME"))
client.drop_database(os.environ.get("MONGO_DB"))
db = client[os.environ.get("MONGO_DB")]
STOCK_API = os.environ.get("STOCK_API")
_30stock = ['ACB', 'BID', 'BVH', 'CTG', 'DHG', 'DPM', 'EIB', 'FPT', 'GAS', 'GMD', 'HDB', 'HPG', 'MBB', 'MSN', 'MWG', 'NVL', 'PNJ', 'REE', 'ROS', 'SAB', 'SBT', 'SSI', 'STB', 'TCB', 'TPB', 'VCB', 'VHM', 'VIC', 'VJC', 'VPB']


def get_data(stock, size):
    query = 'code:' + stock
    params = {
                "sort": "date",
                "size": size,
                # "page": 1,
                "q": query
            }
    headers = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.34',
    }
    # res = requests.get("https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&size=1500&q=code:SSI~date:gte:2021-08-20" , headers = headers)
    res = requests.get( STOCK_API, params = params , headers = headers)
    data = (res.json())['data']
    index = len(data)
    for item in data:
        date_time_str = item['date'] + ' ' + item['time']
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        item['timestamp'] = date_time_obj.timestamp()
        item['index'] = index 
        index = index -1
    sorted_timestamp = sorted(data, key=lambda x: x['timestamp'])
    # for i in sorted_timestamp:
    #   print(i['date'], i['time'], i['timestamp'])
    return sorted_timestamp

def init_get():
    for stock in _30stock:
        result = get_data(stock, os.environ.get("STOCK_SIZE"))
        collection = db[stock]
        for res in result:
            collection.insert_one(res)
    print("DONE INIT INSERT")

def daily_get():
    print("START DAILY GET")
    for stock in _30stock:
        result = get_data(stock , 1)
        collection = db[stock]
        top = collection.find_one(sort=[( '_id', pymongo.DESCENDING )])
        
        if (top is not None) and (top['date'] == result[0]['date']):
            # print("DUPLICATE")
            continue
        collection.insert_one(result[0])

if __name__=='__main__':
    init_get()
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_get, 'interval', seconds=5000)
    scheduler.start()
    app.run(host="0.0.0.0", port=5000)