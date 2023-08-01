from .models import About
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import About_serializers


class about_view(APIView):
    def get(self,request):
        print(About.objects.first())
        return Response(About_serializers(About.objects.all(),many=True,context={'request':request,'user':request.user}).data)
