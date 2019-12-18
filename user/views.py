import os
import sys
import jwt
import json
import bcrypt
import requests
import sqlalchemy.orm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from sqlalchemy.sql               import exists
from sqlalchemy.exc               import IntegrityError
from sqlalchemy.orm.exc           import MultipleResultsFound, NoResultFound

from .models                      import User, ShopInformation, Tag, ShopInformationTagCdMapping
from item.models                  import ShopInformationItemMapping, ItemMaster, ItemImg
from datetime                     import datetime, timedelta
from django.http                  import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views                 import View
from django.core.exceptions       import ValidationError
from django.db                    import IntegrityError

from my_settings                  import ACCESS_TOKEN, REFRESH_TOKEN, createdToken

from clone_back_liter.databases   import Engine, Base, Session

# 공통코드 유저
USER_TYPE = {
    'admin'       : '001',
    'normal'      : '002',
    'advertiser'  : '003'
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
        engine  = Engine("liter")
        base    = Base()
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
                            createdAtDate            = datetime.now(),
                            isAgreed                 = userData['isAgreed']
                        )
                session.add(user)
                session.commit()

            return JsonResponse({"MESSAGE" : "SIGNUP_SUCCESS"}, status=200)		
        except KeyError:
            session.rollback()
            return JsonResponse({"MESSAGE" : "INVALID_KEY"}, status=400)
        except AttributeError:
            return JsonResponse({"MESSAGE" : "INVAILD_EMAIL"}, status=401)
        finally:
            session.close()

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        engine = Engine('liter')
        base = Base()
        session = Session(base, engine)

        try:
            userData      = session.query(User).filter(User.email == data["email"]).filter(User.userLoginTypeCd == data['userLoginTypeCd']).one_or_none() 
            userPassword  = userData.password.encode('utf-8')
            bytedPassword = data['password'].encode('utf-8')

            if bcrypt.checkpw(bytedPassword, userPassword):
                accessToken = createdToken(userData, ACCESS_TOKEN['exp_time'], ACCESS_TOKEN['secret'])
                refreshToken = createdToken(userData, REFRESH_TOKEN['exp_time'], REFRESH_TOKEN['secret'])
                return JsonResponse({"MESSAGE" : "SUCCESS", "ACCESS_TOKEN" : accessToken, "REFRESH_TOKEN" : refreshToken}, status=200)
            else:
                return JsonResponse({"MESSAGE" : "INVALID_PASSWORD"}, status=401)
        except KeyError:
            return JsonResponse({"MESSAGE" : "INVALID_INPUT"}, status=400)
        except AttributeError:
            return JsonResponse({"MESSAGE" : "INVAILD_EMAIL"}, status=401)
        finally:
            session.close()

class GoogleLogInView(View):
    def _getGoogleUserInfo(self, idToken):
        googleApUrl       = "https://oauth2.googleapis.com/tokeninfo?idToken="
        response          = requests.get(googleApUrl + idToken)
        googleUserInfo    = response.json()
        return googleUserInfo

    def post(self, request):
        engine          = Engine("liter")
        base            = Base()
        session         = Session(base, engine)
        googleIdToken   = request.headers.get('Authorization', None)
        
        try:
            if googleIdToken is None:
                return JsonResponse({'message' : 'MISSING_GOOGLE_TOKEN'}, status=400)

            google            = USER_LOGIN_TYPE['google']
            googleUserInfo    = self._getGoogleUserInfo(googleIdToken)
            
            if 'error' in googleUserInfo:
                message = googleUserInfo['error_description']
                return JsonResponse({'message' : message}, status=400)

            user = session.query(User.email).filter(User.email == googleUserInfo['email']).one_or_none() 

            if user is None:
        
                user = User(
                    email                    = googleUserInfo['email'],
                    password                 = 'null',
                    name                     = googleUserInfo['name'],
                    snsid                    = googleUserInfo['sub'],
                    receivingEmail           = 'null',  
                    userTypeCd               = USER_TYPE['normal'], 
                    createdAtDate            = datetime.now(),
                    userLoginTypeCd          = USER_LOGIN_TYPE['google'],
                    isAgreed                 = True
                )
                session.add(user)
                session.commit()

                user = session.query(User).filter(User.snsid == userData['id']).filter(User.userLoginTypeCd == USER_LOGIN_TYPE['google']).one()
                accessToken  = createdToken(user, ACCESS_TOKEN['exp_time'], ACCESS_TOKEN['secret'])
                refreshToken = createdToken(user, REFRESH_TOKEN['exp_time'], REFRESH_TOKEN['secret'])
                return JsonResponse({"MESSAGE" : "SUCCESS", "ACCESS_TOKEN" : accessToken, "REFRESH_TOKEN" : refreshToken}, status=200)

            else :
                user = session.query(User).filter(User.snsid == userData['id']).filter(User.userLoginTypeCd == USER_LOGIN_TYPE['google']).one()
                accessToken  = createdToken(user, ACCESS_TOKEN['exp_time'], ACCESS_TOKEN['secret'])
                refreshToken = createdToken(user, REFRESH_TOKEN['exp_time'], REFRESH_TOKEN['secret'])
                return JsonResponse({"MESSAGE" : "SUCCESS", "ACCESS_TOKEN" : accessToken, "REFRESH_TOKEN" : refreshToken}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "INVALID_INPUT"}, status=401)

        finally:
            session.close()

class KakaoSignInView(View):
    def post(self, request):
        engine = Engine('liter')
        base = Base()
        session = Session(base, engine)
        if not "Authorization" in request.headers.keys():
            return JsonResponse({"MESSAGE" : "INVALID_KAKAO_TOKEN"}, status=401)
        
        kakao_token  = request.headers["Authorization"]
        headers      = ({'Authorization' : f"Bearer {kakao_token}"})
        url          = "https://kapi.kakao.com/v1/user/me"
        response     = requests.post(url, headers=headers, timeout=2)
        userData     = response.json()
        try:
            if session.query(User).filter(User.snsid == userData['id']).filter(User.userLoginTypeCd == USER_LOGIN_TYPE['kakao']).one():
                user = session.query(User).filter(User.snsid == userData['id']).filter(User.userLoginTypeCd == USER_LOGIN_TYPE['kakao']).one()
                accessToken = createdToken(user, ACCESS_TOKEN['exp_time'], ACCESS_TOKEN['secret'])
                refreshToken = createdToken(user, REFRESH_TOKEN['exp_time'], REFRESH_TOKEN['secret'])
                return JsonResponse({"MESSAGE" : "SUCCESS", "ACCESS_TOKEN" : accessToken, "REFRESH_TOKEN" : refreshToken}, status=200)
                
            else:
                signupUser = User(
                    email              = userData['kaccount_email'],
                    userLoginTypeCd    = USER_LOGIN_TYPE['kakao'],
                    userTypeCd         = USER_TYPE['normal'],
                    snsid              = userData['id'],
                    name               = userData['properties']['nickname'],
                    isAgreed           = userData['kaccount_email_verified'],
                    createdAtDate      = datetime.datetime.now(),
                    password           = None,
                    receivingEmail     = None
                    )
                session.add(signupUser)
                session.commit()
                accessToken = createdToken(signupUser, ACCESS_TOKEN['exp_time'], ACCESS_TOKEN['secret'])
                refreshToken = createdToken(signupUser, REFRESH_TOKEN['exp_time'], REFRESH_TOKEN['secret'])
                return JsonResponse({"MESSAGE" : "SUCCESS", "ACCESS_TOKEN" : accessToken, "REFRESH_TOKEN" : refreshToken}, status=200)
        
        except KeyError:
            session.rollback()
            return JsonResponse({"MESSAGE" : "INVALID_INPUT"}, status=401)
        finally:
            session.close()

class FacebookSignInView(View):
    def post(self, request):
        engine = Engine('liter')
        base = Base()
        session = Session(base, engine)
        facebook_token = request.headers["Authorization"]
               
        url             = 'https://graph.facebook.com/me'
        userInforField  = [
            'id',
            'name',
            'email'
        ]
        paramUserInfor = {
            "fields" :','.join(userInforField),
            "access_token" : facebook_token
        }
        response       = requests.get(url, params=paramUserInfor, timeout=2)
        userData       = response.json()
        
        try:
            if session.query(exists().where(User.snsid == userData['id'])).scalar():
                user = session.query(User).filter(User.snsid == userData['id']).filter(User.userLoginTypeCd == USER_LOGIN_TYPE['facebook']).one()
                accessToken  = createdToken(user, ACCESS_TOKEN['exp_time'], ACCESS_TOKEN['secret'])
                refreshToken = createdToken(user, REFRESH_TOKEN['exp_time'], REFRESH_TOKEN['secret'])
                return JsonResponse({"MESSAGE" : "SUCCESS", "ACCESS_TOKEN" : accessToken, "REFRESH_TOKEN" : refreshToken}, status=200)
            else:
                signupUser = User(
                    email              = userData['email'],
                    userLoginTypeCd    = USER_LOGIN_TYPE['facebook'],
                    userTypeCd         = USER_TYPE['normal'],
                    snsid              = userData['id'],
                    name               = userData['name'],
                    isAgreed           = True,
                    createdAtDate      = datetime.datetime.now(),
                    password           = None,
                    receivingEmail     = None
                    )
                session.add(signupUser)
                session.commit()
                accessToken = createdToken(user, ACCESS_TOKEN['exp_time'], ACCESS_TOKEN['secret'])
                refreshToken = createdToken(user, REFRESH_TOKEN['exp_time'], REFRESH_TOKEN['secret'])
                return JsonResponse({"MESSAGE" : "SUCCESS", "ACCESS_TOKEN" : accessToken, "REFRESH_TOKEN" : refreshToken}, status=200)
        except KeyError:
            session.rollback()
            return JsonResponse({"MESSAGE" : "INVALID_INPUT"}, status=400)
        except ValueError:
            session.rollback()
            return JsonResponse({"MESSAGE" : "INVALID_KAKAO_ACCESS_TOKEN"}, status=401)
        finally:
            session.close()



class ShopInformationView(View):
    def get(self, request):        
        engine = Engine('liter')
        base   = Base()
        session = Session(base, engine)
        
        try:
            shopInfo = (session.query(ShopInformation.shopId, ShopInformation.shopTi, ShopInformation.shopSubTi, ShopInformation.shopTiImg)
            .filter(ShopInformationItemMapping.shopId == 1 and ShopInformationItemMapping.tagId == 1).one())

            tagInfo = (session.query(Tag.tagId, Tag.tagName)
            .filter(ShopInformationItemMapping.shopId == 1).all())
            listedTagInfo = [ { "tagId" : i, "tagName" : j } for i, j in tagInfo]

            itemInfo = (session.query(ItemMaster.itemId, ItemMaster.itemTi , ItemMaster.endDate ,ItemImg.itemImg)
            .filter(ShopInformationItemMapping.shopId == 1).filter(ItemMaster.itemId == ItemImg.itemImgId).all()
            )
            listeditemInfo = [ { "itemId" : a, "itemTi" : b, "time": c, "itemImg": d} for a, b, c, d in itemInfo]

            result = {  
            "shopId"      : shopInfo.shopId,
            "shopTi"      : shopInfo.shopTi,
            "shopSubTi"   : shopInfo.shopId,
            "shopTiImg"   : shopInfo.shopTiImg,
            "shopTypeCd"  : listedTagInfo,
            "item"        : listeditemInfo
            }
            return JsonResponse(result, status=200)

        except KeyError:
            session.rollback()
            return JsonResponse({"MESSAGE" :  "INVALID_INPUT"}, status=400)

        except ValueError:
            session.rollback()
            return JsonResponse({"MESSAGE" : "VALUE_NOT_EXIST"}, status=401)

        except AttributeError:
            session.rollback()
            return JsonResponse({"MESSAGE" : "ATTRIBUTE_NOT_EXIST"}, status=401)

        finally:
            session.close()
