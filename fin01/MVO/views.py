from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import os
import json
from django.conf import settings
from dotenv import load_dotenv
load_dotenv(os.path.join(settings.BASE_DIR, '.env'))

import requests
# Create your views here.
def index(request):
    if(request.method == "GET"):
        return render(request,'MVO/index.html' , {'stocks' : settings.STOCKS} )
    if(request.method == "POST"):
        API = os.environ.get("MVO_API") + ":" + os.environ.get("MVO_PORT")
        res = requests.get("http://" + API + "/mvo" , json={
            "tickers" : request.POST.getlist("tickers[]"),
            "start_date" : request.POST.get("start_date"),
            "end_date" : request.POST.get("end_date"),
        })
        res = res.json()
        for key in res:
            if (key != 'corr_matrix') and (not isinstance(res[key] , dict)):
                res[key] = json.loads(res[key])

        
        return JsonResponse(res)
        