from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.models import Mago, Modalidad
from user.serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMiPerfil(request):
    # try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk=id_usuario)
        serializer = MagoProfileSerializer(mago, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # except:
    #     return Response(
    #         {"detail": "Usuario no autorizado"},
    #         status=status.HTTP_401_UNAUTHORIZED
    #     )


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
def crearModalidad(request):
    try:
        if(Modalidad.objects.filter(nombre=request.data['nombre']).count() == 0):
            modalidad = Modalidad.objects.create(nombre=request.data['nombre'])
            serializer = createModalidadesSerializer(modalidad, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
            {"detail": "La modalidad ya existe"},
            status=status.HTTP_400_BAD_REQUEST
        )
    except:
        return Response(
            {"detail": "La modalidad no se ha podido crear"},
            status=status.HTTP_400_BAD_REQUEST
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listadoMagos(request):
    try:
        id_usuario = request.user.id
        admin = Mago.objects.get(username= 'admin')
        lista_magos = Mago.objects.all().exclude(id= id_usuario).exclude(id= admin.id)
        serializer = listadoMagosSerializer(lista_magos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Usuario no autorizado"},
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verPerfilMago(request, id):
    try:
        mago = Mago.objects.get(id= id)
        serializer = verPerfilMagoSerializer(mago, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Usuario no autorizado"},
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMisAmigos(request):
    try:
        id_usuario = request.user.id
        amigos = Mago.objects.get(id= id_usuario).amigos
        serializer = listadoMagosSerializer(amigos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Usuario no autorizado"},
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buscarMago(request):
    try:
        id_usuario = request.user.id
        admin = Mago.objects.get(username= 'admin')
        lista_magos = Mago.objects.all().exclude(id= id_usuario).exclude(id= admin.id)
        nombre = request.data['nombre']
        modalidades = request.data['modalidades']
        if nombre != '':
            lista_magos = lista_magos.filter(nombre__icontains=nombre)
        if modalidades:
            for id_ in modalidades:
                lista_magos = lista_magos.filter(modalidades__in=[id_]).distinct()
        serializer = listadoMagosSerializer(lista_magos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Usuario no autorizado"},
            status=status.HTTP_401_UNAUTHORIZED
        )

