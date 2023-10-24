from django.shortcuts import render, redirect
from datetime import datetime
# Create your views here.
from django.http import JsonResponse
import os
from django.conf import settings
from dotenv import load_dotenv
load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
from pymongo import MongoClient
def get_stock(request, stock):
  client = MongoClient(host=os.environ.get("MONGO_HOST"),
                     port=int(os.environ.get("MONGO_PORT")), 
                     username=os.environ.get("MONGO_USERNAME"),
                     password=os.environ.get("MONGO_PASSWORD"),
                     authSource=os.environ.get("MONGO_USERNAME"))
  db = client[os.environ.get("MONGO_DB")]
  data = []
  for item in db[stock].find():
    del item['_id']
    # del item['timestamp']
    # date_time_str = item['date'] + ' ' + item['time']
    # date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    # item['timestamp'] = date_time_obj.timestamp()
    data.append(item)
  return JsonResponse({'data' : data})


def dashboard(request):
  return render(request , 'home/dashboard.html' , context={'user' : request.user.username , 'balance' : round(request.user.balance,2) , 'stocks' : settings.STOCKS})


