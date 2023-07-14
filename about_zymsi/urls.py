
from django.urls import path
from .views import about_view

urlpatterns = [
    path('about_zymsi/',about_view.as_view())

]