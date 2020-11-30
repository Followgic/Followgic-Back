from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from user.models import Mago
from user.serializers import MagoSerializer



@api_view(['GET'])
def listarMagos(request):
    magos = Mago.objects.all()
    serializer = MagoSerializer(magos, many=True)
    #permission_classes = [permissions.IsAuthenticated]
    return Response(serializer.data)
    
