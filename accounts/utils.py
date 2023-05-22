import jwt, pyotp
from datetime import timedelta, datetime
from accounts.models import User
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

def generate_key():
    """ User otp key generator """
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    generate_key()


def is_unique(key):
    try:
        User.objects.get(key=key)
    except User.DoesNotExist:
        return True
    return False

def get_short_lived_token(user):
    refresh_token = RefreshToken.for_user(user)
    return str(refresh_token)


def get_token(user):
    refresh_token = RefreshToken.for_user(user)
    refresh_token.set_exp(lifetime=timedelta(days=30))  # EXTEND lifetime
    return str(refresh_token)


def generate_custom_short_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=0, minutes=120),
        'iat': datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token


def get_user(access_token):
    payload = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=['HS256'])
    return payload['user_id']
