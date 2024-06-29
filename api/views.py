from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from api.serializers import CakeSerializer

from kart.models import Cake

# Create your views here.

class CakeListView(APIView):

    def get(self,request,*args,**kwargs):

        qs=Cake.objects.all()

        serializer_instance=CakeSerializer(qs,many=True)

        return Response(data=serializer_instance.data)
    