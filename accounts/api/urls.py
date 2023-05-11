from django.contrib import admin
from django.urls import path
from accounts.api.api_view import login


urlpatterns = [
    path('', login.as_view()),

]