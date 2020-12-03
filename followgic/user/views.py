from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.models import Mago
from user.serializers import MagoProfileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMiPerfil(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        serializer = MagoProfileSerializer(mago, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Usuario no autorizado"},
            status = status.HTTP_401_UNAUTHORIZED
        )
