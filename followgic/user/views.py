from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.models import Mago
from user.serializers import MagoSerializer



@api_view(['GET'])
def verMiPerfil(request):
    try:
        usuario = request.user
        magos = Mago.objects.get(usuario=usuario)
        serializer = MagoSerializer(magos, many=False)
        return Response(serializer.data)
    except:
        return Response(
            {"detail": "Usuario no autorizado"},
            status = status.HTTP_401_UNAUTHORIZED
        )
