from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User
import pyotp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import random

class login(APIView):
    permission_classes = [AllowAny]

    def EmailSending(self, sender_email, text=None):
        email= 'yashrasniya3@gmail.com'
        password='#Ar4Chi7!'
        html=None
        subject='subject'
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = email
        message["To"] = sender_email
        if text:
            part1 = MIMEText(text, "plain")
            message.attach(part1)
        if html:
            part2 = MIMEText(html, "html")
            message.attach(part2)

        context = ssl.create_default_context()
        # showwarning('error', 'code is commented')
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email, password)
                server.sendmail(
                    sender_email, sender_email, message.as_string()
                )

        except smtplib.SMTPRecipientsRefused as e:
            print('error')

    def error(self,message):
        return {'error':message,'status':False}
    def get(self,request):
        email = request.GET.get('email', None)
        if not email:
            return Response(self.error('email not found'))
        user_obj=User.objects.filter(mob_number=email)
        if not user_obj:
            return Response(self.error('User not found'))



        # generate OTP
        time_otp=str(random.randint(1000,9999))
        # if email != "1988888888":
        #     self.EmailSending(email,time_otp)
        return Response({'status': '200', 'message': 'Please verify your mobile to complete signup.','otp':time_otp},
                        status.HTTP_200_OK)

