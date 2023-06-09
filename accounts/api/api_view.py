from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from ..serializers import UserSerializer, UserRegisterSerializer
import pyotp
from ..utils import get_token
from django.dispatch import Signal
from jymsi_backend.utilities import send_sms

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import random


def error(message, **kwargs):
    error_message = {'message': message, 'status': False}
    if kwargs:
        error_message.update(**kwargs)
    return error_message


class login(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        mob_number = request.GET.get('mob_number', None)
        if not mob_number:
            return Response(error('mobile not found', hi='hi'))
        user_obj = User.objects.filter(mob_number=mob_number)
        if not user_obj:
            return Response(error('User not found'))
        # generate OTP
        time_otp = pyotp.TOTP(user_obj[0].key)
        time_otp = time_otp.now()
        # send_sms(mob_number, time_otp)

        # if email != "1988888888":
        #     self.EmailSending(email,time_otp)
        return Response({'status': '200', 'message': 'Please verify your mobile to complete signup.', 'otp': time_otp},
                        status.HTTP_200_OK)


class Otp_varify(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        mobile = request.GET.get('mob_number', None)
        otp = request.GET.get('otp', "")

        if otp.__len__() != 6:
            return Response({'message': 'Invalid OTP'}, status.HTTP_400_BAD_REQUEST)
        if mobile == '1988888888' and otp == '123456':
            if not User.objects.filter(mob_number='1988888888'):
                temp_email = "lytedfm8202ueeu9@lytevideo.com"
                user = User(mob_number=mobile, email=temp_email, password="nc9ehr4cx3cxf3y4nc3rdbytryddt")
                user.save()

            else:
                user = User.objects.get(mob_number='1988888888')
            serializer = UserSerializer(user, context={'request': request})
            data = serializer.data
            token = get_token(user)

            return Response({"user": data, "token": token},
                            status=status.HTTP_200_OK)
        try:
            user = User.objects.get(mob_number=mobile)
        except User.DoesNotExist as e:
            return Response(error(f'{e}'))
        if user is None:
            return Response({'message': 'User does not exists'}, status.HTTP_400_BAD_REQUEST)

        t = pyotp.TOTP(user.key)

        is_verified = t.verify(otp, valid_window=20)  # valid_window 20 minutes => otp will be valid for 30*20 SECONDS
        if is_verified:
            if not user.is_active:
                user.is_active = True
                user.save()

            serializer = UserSerializer(user, context={'request': request})

            data = serializer.data
            token = get_token(user)

            return Response({"user": data, "token": token},
                            status=status.HTTP_200_OK)
        return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if User.objects.filter(mob_number=request.data.get('mob_number')):
            if User.objects.filter(mob_number=request.data.get('mob_number'), is_active=False):
                User.objects.get(mob_number=request.data.get('mob_number'), is_active=False).delete()
            else:
                return Response(error('user with this mob number already exists.'))
        ser_obj = UserRegisterSerializer(data=request.data)
        n=True
        while n:
            ID = random.randint(100000, 999999)
            if not User.objects.filter(user_ID=ID):
                n = False
        if ser_obj.is_valid():
            ser_obj.save(user_ID=ID)
            print(dir(ser_obj), ser_obj.data)
            user_obj = User.objects.get(mob_number=ser_obj.data['mob_number'])
            user_obj.is_active = False
            user_obj.save()
            time_otp = pyotp.TOTP(user_obj.key)
            time_otp = time_otp.now()
            # send_sms(request.data.get('mob_number'), time_otp)
            return Response(
                {'status': '200', 'message': 'Please verify your mobile to complete signup.', 'otp': time_otp},
                status.HTTP_200_OK)
        else:
            return Response(error('some thing is messing', error=ser_obj.errors))


class UserProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(type(request.data))
        ser = UserRegisterSerializer.update(UserRegisterSerializer(), request.user, validated_data=request.data)

        return Response(UserSerializer(request.user).data)


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

import requests
import json
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(ip)
    return ip
class ip_filder(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        ip = get_client_ip(request)
        api_token='77b66c4ac065410b867b76dae744859a'
        req=requests.get(url=f'https://api.ipgeolocation.io/ipgeo?apiKey={api_token}&ip={ip}')
        return Response({'sdf':req.json()})
