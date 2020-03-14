import json
from datetime import datetime as dt
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.http import JsonResponse
from django.conf import settings 

from manager import OrderManager

def order_request(request):
    req_dir = os.path.join(settings.BASE_DIR, 'watcher/order_requests')
    res_dir = os.path.join(settings.BASE_DIR, 'watcher/order_responses')
    
    manager = OrderManager(req_dir, res_dir)
    data =  manager.run(request)
    return data