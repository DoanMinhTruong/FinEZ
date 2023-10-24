import os
import pandas as pd
from os.path import join, dirname
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
def get_data(tickers, start_date, end_date):
    client = MongoClient(host=os.environ.get("MONGO_HOST"),
                        port=int(os.environ.get("MONGO_PORT")), 
                        username=os.environ.get("MONGO_USERNAME"),
                        password=os.environ.get("MONGO_PASSWORD"),
                        authSource=os.environ.get("MONGO_USERNAME"))
    db = client[os.environ.get("MONGO_DB")]
    query = {
        "date": {
            "$gte": start_date,
            "$lte": end_date
        }
    }
    df = pd.DataFrame(columns = ['Date'] + tickers)
    for ticker in tickers:
        lst = []
        date = []
        col = db[ticker]
        for document in col.find(query):
            del document['_id']
            lst.append(document['close'])
            date.append(document['date'])
        df[ticker] = lst
        if(df['Date'].isnull().values.any()):
            df['Date'] = date
    df['Date'] = pd.to_datetime(df['Date'])
    
    df = df.set_index('Date')
    return df
# print(get_data(["ACB" , "VCB", "FPT"] , "2023-10-10", "2023-10-20"))