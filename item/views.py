import json
import sqlalchemy.orm

from .models                      import ItemMaster

from django.http                  import JsonResponse, HttpResponse
from django.core.exceptions       
from django.db                    

from clone_back_liter.databases

# 공통코드 아이템
ITEM_STATE = {
    'newItem'  : '400',
    'usedItem' : '401',
}

ITEM_VAT_TYPE = {
    'taxation'  : '402',
    'taxFree'   : '403'
}

ITEM_BIZ_CLASS = {
    'corporation'  : '404',
    'selfEmployed' : '405' # 개인사업자
}

ITEM_RECIEPT = {
    'salesCheckOfCreaditCard' : '406',
    'onlineCashReceipts'      : '407'
}


class ShopInformationView(View):
    def get(self, request):


    def post(self, request):
