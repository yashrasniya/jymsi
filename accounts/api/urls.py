from django.contrib import admin
from django.urls import path
from accounts.api.api_view import (login, Otp_varify,
                                   register, UserProfileUpdate,
                                   UserProfile)

urlpatterns = [
    path('login/', login.as_view()),
    path('otp_varify/', Otp_varify.as_view()),
    path('register/', register.as_view()),
    path('profile/update/', UserProfileUpdate.as_view()),
    path('profile/', UserProfile.as_view()),

]
