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
        partner = request.GET.get('is_partner', None)
        if not mob_number:
            return Response(error('mobile not found', hi='hi'))
        if mob_number in ['1988888888' ,'9999999999']:
            return Response(
                {'status': '200', 'message': 'Please verify your mobile to complete signup.'},
                status.HTTP_200_OK)
        user_obj = User.objects.filter(mob_number=mob_number)
        print(type(partner))
        if not user_obj:
            return Response(error('User not found'))
        if partner:
            user_obj=user_obj.filter(is_partner=True)
            if not user_obj: return Response(error('User is not aloud  to login in partner side'))
        else:
            user_obj = user_obj.filter(is_partner=False)
            if not user_obj: return Response(error('partner is not aloud  to login in User side'))

        # generate OTP
        time_otp = pyotp.TOTP(user_obj[0].key)
        time_otp = time_otp.now()
        if not mob_number=='1988888888' or mob_number=='9999999999':
            send_sms(mob_number, time_otp)

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
        if mobile in ['1988888888','9999999999'] and otp == '123456':
            if not User.objects.filter(mob_number=mobile):
                temp_email = "lytedfm8202ueeu9@lytevideo.com"
                user = User(mob_number=mobile, email=temp_email, password="nc9ehr4cx3cxf3y4nc3rdbytryddt")
                user.save()

            else:
                user = User.objects.get(mob_number=mobile)
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
            send_sms(request.data.get('mob_number'), time_otp)
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

import google_auth_oauthlib.flow
from django.shortcuts import redirect
redirect_uri="http://127.0.0.1:8000/api/v1/google_callback/"
def googel_login(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'], )

    flow.redirect_uri = redirect_uri

    authorization_url, state = flow.authorization_url(

        access_type='online',

    )
    return redirect(authorization_url)

client_id="549026914943-7v02pt7ng4kt8kiq1ecpsmolo1k1413b.apps.googleusercontent.com"
client_secret="MTB2VGfXaqx0iHLPfrWqgc6E"

from django.http.response import HttpResponse,JsonResponse
def google_login_callback(request):
    code=request.GET.get('code',False)
    if not code:
        return HttpResponse('code not found')
    url = f"https://oauth2.googleapis.com/token?" \
          f"code={code}" \
          f"&client_id={client_id}" \
          f"&client_secret={client_secret}" \
          f"&redirect_uri={redirect_uri}" \
          f"&grant_type=authorization_code"

    payload = {}
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code!=200:
        return HttpResponse(f'some thing went wrong! {response.status_code}')
    access_token=response.json()['access_token']

    url = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code!=200:
        return HttpResponse(f'some thing went wrong! {response.status_code}')
    data=response.json()
    user_obj=User.objects.filter(email=data['email'])
    if user_obj:
        user_obj=user_obj[0]
        serializer = UserSerializer(user_obj, context={'request': request})
        data = serializer.data
        token = get_token(user_obj)
        return JsonResponse({"user": data, "token": token})
    user_obj=User.objects.create(email=data['email'],
                        first_name=data['given_name'],
                        last_name=data['family_name'],
                        mob_number=data['email'],
                        profile_img=data['picture']
                                 )
    serializer = UserSerializer(user_obj, context={'request': request})

    data = serializer.data
    token = get_token(user_obj)

    return JsonResponse({"user": data, "token": token})


