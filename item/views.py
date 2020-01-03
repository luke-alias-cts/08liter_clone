import os
import sys
import json
import requests
import dateutil.parser
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from datetime                     import datetime
from item.models                  import ItemMaster, ItemImg, ItemInformationImg, ItemOption

from django.views                 import View
from django.http                  import JsonResponse, HttpResponse, HttpRequest
from sqlalchemy.orm.exc           import NoResultFound

from clone_back_liter.databases   import Engine, Base, Session

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
    'corporation'  : '404',# 법인사업자
    'selfEmployed' : '405' # 개인사업자
}

ITEM_RECIEPT = {
    'salesCheckOfCreaditCard' : '406',
    'onlineCashReceipts'      : '407'
}


class ItemView(View):
    def get(self, request):
        
        engine  = Engine("liter")
        base    = Base()
        session = Session(base, engine)
        itemId  = request.GET.get("itemId", None)

        try:
            item           = session.query(ItemMaster).filter(ItemMaster.itemId == itemId).one()
            itemImgs       = session.query(ItemImg).filter(ItemImg.itemMasterId == itemId).all()
            itemInforImgs  = session.query(ItemInformationImg).filter(ItemInformationImg.itemMasterId == itemId).all()
            itemOptions    = session.query(ItemOption).filter(ItemOption.itemMasterId == itemId).all()
            result = {
                "itemId"               : item.itemId,
                "itemTi"               : item.itemTi,
                "itemImg"              : [{ "url" : element.itemImg }for element in itemImgs],
                "itemInformationImg"   : [ element.itemInformationImg for element in itemInforImgs], 
                "price"                : item.price,
                "discount"             : item.discount,
                "endDate"              : item.endDate.strftime("%Y-%m-%d %H:%M:%S"),
                "optionDescription"    : item.optionDescription,
                "itemState"            : item.itemStateCd,
                "itemVatTypeCd"        : item.vatTypeCd,
                "itemReceipt"          : item.itemReceiptCd,
                "itemBizClass"         : item.itemBizClassCd,
                "ori"                  : item.ori,
                "madeInYear"           : item.madeInYear,
                "maIm"                 : item.maIm,
                "managerTel"           : item.managerTel,
                "cauOfUse"             : item.cauOfUse,
                "special"              : item.special,
                "mat"                  : item.mat,
                "sizeVolume"           : item.sizeVolume,
                "madeIn"               : item.madeIn,
                "expiryDate"           : item.expiryDate,
                "optionName"           : [element.optionName for element in itemOptions] ,
                "targetQuantity"       : [element.targetQuantity for element in itemOptions],
                "salesOfItem"          : [element.salesOfItem for element in itemOptions], 
                "stock"                : [element.stock for element in itemOptions],
                "optionPrice"          : [element.optionPrice for element in itemOptions], 
            }
            return JsonResponse({"DATA" : result}, status=200)
        except NoResultFound:
            return JsonResponse({"MESSAGE" : "NOT_FOUND_ITEM"}, status=404)
        except KeyError:
            return JsonResponse({"AAA" : "FAULT"}, status=400)
        finally:
            session.close()