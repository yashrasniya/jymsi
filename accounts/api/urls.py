from django.contrib import admin
from django.urls import path
from accounts.api.api_view import (login, Otp_varify,
                                   register, UserProfileUpdate,
                                   UserProfile,ip_filder,googel_login,
                                   google_login_callback,
                                   Mobile_number_verify,
                                   OTP_verify)

urlpatterns = [
    path('login/', login.as_view()),

    path('otp_varify/', Otp_varify.as_view()),
    path('register/', register.as_view()),
    path('profile/update/', UserProfileUpdate.as_view()),
    path('profile/', UserProfile.as_view()),

    path('ip/', ip_filder.as_view()),

    path('googlelogin/', googel_login),
    path('google_callback/', google_login_callback),
    path('mobile/otp_send/',Mobile_number_verify.as_view() ),
    path('mobile/otp_verify/', OTP_verify.as_view()),

]
