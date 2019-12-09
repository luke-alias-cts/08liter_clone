import os
import sys
import jwt
import json
import bcrypt
import requests
import datetime
import sqlalchemy.orm

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from .models                      import User, ShopInformation

from django.http                  import JsonResponse, HttpResponse
from django.views                 import View
from django.core.validators       import validate_email
from django.core.exceptions       import ValidationError
from django.db                    import IntegrityError

from clone_back_liter.databases   import Engine, Base, Session

# 공통코드 유저
USER_TYPE = {
    'admin'       : '001',
    'normal'      : '002',
    'influencer'  : '003',
    'advertiser'  : '004'
}
USER_LOGIN_TYPE = {
    'homepage'    : '010',
    'kakao'       : '011',
    'google'      : '012',
    'facebook'    : '013'
}

class SignupView(View):

    def post(self, requests):
        userData = json.loads(requests.body)
        engine = Engine("tests")
        base   = Base()
        session = Session(base, engine)

        try:

            if session.query(User.email).filter(User.email == userData["email"]).one_or_none():                
                return JsonResponse({"MESSAGE" : "THIS_IS_EMAIL_ALREADY_EXIST"}, status=400)

            else :
                bytedPassword  = bytes(userData["password"], encoding='utf-8')
                hashedPassword = bcrypt.hashpw(bytedPassword, bcrypt.gensalt())
                decodePassword = hashedPassword.decode('utf-8')
                
                user = User(
                            email                    = userData['email'],
                            password                 = decodePassword,
                            name                     = userData['name'],
                            snsid                    = userData['snsid'],
                            receivingEmail           = userData['receivingEmail'],
                            userLoginTypeCd          = userData['userLoginTypeCd'],
                            userTypeCd               = userData['userTypeCd'], 
                            createdAtDate            = datetime.datetime.now()
                        )
                session.add(user)
                session.commit()

            return JsonResponse({"MESSAGE" : "SIGNUP_SUCCESS"}, status=200)
		
        except ValidationError:
            return JsonResponse({"MESSAGE" : "NOT_EMAIL_FORM"}, status =400)
		
        except KeyError:
            return JsonResponse({"MESSAGE" : "INVALID_KEY"}, status=400)
        

class ShopInformationView(View):
    def post(self, request):
        data = json.loads(request.body)
        engine = Engine('tests')
        base   = Base()
        session = Session(base, engine)
        user = request.user

        try:
            shopinfor = ShopInformation(
                shopTi      = data['shopTi'],
                shopSubTi   = data['shopSubTi'],
                shopTiImg   = data['shopTiImg']
            )
            session.add(shopinfor)
            session.commit()

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
        except IntegrityError:
            return JsonResponse({"MESSAGE" : "USER_HAS_ALREADY_SHOP"}, status=409)
        except KeyError:
            return JsonResponse({"MESSAGE" :  "INVALID_INPUT"}, status=400)