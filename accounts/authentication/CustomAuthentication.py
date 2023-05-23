from accounts.models import User
from rest_framework import authentication
import jwt
import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from rest_framework import status


class PartnerAuthentication(JWTAuthentication):
    def authenticate(self, request, error=True):
        # print('do')
        # if request.META.get('HTTP_AUTHORIZATION', ''):
        #
        #     user_data = jwt.decode(request.META.get('HTTP_AUTHORIZATION').split(' ')[1], settings.SECRET_KEY,
        #                            algorithms=["HS256"])
        #     print(user_data['user_id'])
        #     user = User.objects.get(id=user_data['user_id'])
        #     print(user)
        #     if not user.is_partner:
        #         print("dsfasd")
        #         return None
        super().authenticate(request)


class CustomAuthenticationJwt(JWTAuthentication):
    def authenticate(self, request, error=True):
        header = self.get_header(request)
        if header is None:
            return None if error else (0, False)
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None if error else (0, False)
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

    def get_validated_token(self, raw_token):
        messages = []

        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                print(AuthToken(raw_token))
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})

        raise CustomInvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })


class CustomInvalidToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Token is invalid or expired')
    default_code = 'token_not_valid'
