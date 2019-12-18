import jwt
from datetime import datetime, timedelta

ACCESS_TOKEN = {
        'secret'   : 'Y_LA|sPi/x4)NM2.KB|9T.j`A}M;*Inhg}^<4-v/s=WbHeQYxs',
        'exp_time' : datetime.now() + timedelta(seconds = 60 * 60 * 24),
        }
REFRESH_TOKEN = {
            'secret'   : '}[R~R(#>mklcgxKElkh9]l3-!(jptP]<TamxbDNZ9tML[Ov8B',
            'exp_time' : datetime.now() + timedelta(seconds = 60 * 60 * 24 * 60)
    }

def createdToken(userData, exp, secret):
    payload = {
            'userid'   : userData.userid,
            'exp'      : exp
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    token = token.decode('utf-8')
    return token 

# 어디것으로?
AWS_S3 = {
        'AWS_S3_KEY_ID' : '22', 
        'AWS_S3_ACCESS_KEY' : '22' 
}