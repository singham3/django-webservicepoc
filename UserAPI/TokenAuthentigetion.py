from rest_framework.authentication import get_authorization_header
from .models import *
import jwt
from datetime import datetime, timedelta

token_key = eval(open('config/secret-key.json', 'r').read())


def user_token_authentication(request):
    auth = get_authorization_header(request).split()
    if not auth or auth[0].lower() != b'token': 
        return None

    if len(auth) == 1: 
        return {"Error": 'Invalid token header. No credentials provided.', "status": 403}
    elif len(auth) > 2: 
        return {"Error": 'Invalid token header', "status": 403}

    try: 
        token = auth[1]
        if token == "null": 
            return {"Error": "Null token not allowed", "status": 403}
    except UnicodeError: 
        return {"Error": 'Invalid token header. Token string should not contain invalid characters.', "status": 403}

    return authenticate_credentials(token)


def authenticate_credentials(token): 
    payload = jwt.decode(token, token_key["token_key"])

    email = payload['email']
    account_id = payload['account_id']
    username = payload['username']
    token_created_at = payload['token_created_at']
    try: 
        if datetime.now() - datetime.strptime(str(token_created_at), '%Y-%m-%d %H:%M:%S.%f') > timedelta(seconds=10):
            return {"Error": 'Token Time Out', "status": 408}
        user = User.objects.using('default').get(username=username, email=email, account_id=account_id,
                                                 is_superuser=True, is_staff=True, is_active=True)
        if not user.token == token.decode(): 
            return {"Error": 'Token Mismatch', "status":  403}

    except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError: 
        return {"Error":  'Token is invalid', "status":  403}
    except User.DoesNotExist: 
        return {"Error": 'Internal server error', "status":  403}
    return user
