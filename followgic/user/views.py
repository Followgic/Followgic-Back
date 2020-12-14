from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.models import Mago, Modalidad
from user.serializers import MagoProfileSerializer, ModalidadesSerializer, FotoMagoSerializer, MagoCreateSerializer
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMiPerfil(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk=id_usuario)
        serializer = MagoProfileSerializer(mago, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Usuario no autorizado"},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
def getModalidades(request):
    try:
        modalidades = Modalidad.objects.all()
        serializer = ModalidadesSerializer(modalidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Modalidades no encontradas"},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setImagenMago(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk=id_usuario)
        imagen = request.data['foto']
        mago.foto = imagen
        mago.save()
        serializer = MagoProfileSerializer(mago, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Usuario no autorizado"},
            status=status.HTTP_401_UNAUTHORIZED
        )



