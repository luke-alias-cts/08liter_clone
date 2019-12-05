import os
import sys
import jwt
import json
import bcrypt
import requests
import datetime
import sqlalchemy.orm

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from .models                      import User

from django.http                  import JsonResponse, HttpResponse
from django.views                 import View
from django.core.validators       import validate_email
from django.core.exceptions       import ValidationError

from clone_back_liter.databases   import Engine, Base, Session

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
                            forReceivingEmail        = userData['forReceivingEmail'],
                            companyTf                = userData['companyTf'],
                            influencerTf             = userData['influencerTf'],
                            createdAtYearDate        = datetime.datetime.now()
                        )
                session.add(user)
                session.commit()

            return JsonResponse({"MESSAGE" : "SIGNUP_SUCCESS"}, status=200)
		
        except ValidationError:
            return JsonResponse({"MESSAGE" : "NOT_EMAIL_FORM"}, status =400)
		
        except KeyError:
            return JsonResponse({"MESSAGE" : "INVALID_KEY"}, status=400)
        



