from django.shortcuts import render
from .models import About
from django.http import HttpResponse
from django.http import JsonResponse
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
# Create your views here.

class about_view(APIView):
    def get(self,request):
        print(About.objects.first())
        return Response(About.objects.all().values())
