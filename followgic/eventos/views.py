from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from user.models import *
from datetime import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crearEvento(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)

        evento = Evento()
        evento.titulo = request.data['titulo']
        evento.tipo = request.data['tipo']
        if(request.data['tipo'] == 0):
            evento.link_conferencia = request.data['link_conferencia']
        evento.descripcion = request.data['descripcion']
        evento.fecha_creacion = datetime.now()
        evento.fecha_evento = request.data['fecha_evento']
        evento.hora_evento = request.data['hora_evento']
        evento.aforo = request.data['aforo']
        evento.foto = request.data['foto']
        evento.creador = mago
        evento.save()

        serializer = crearEventoSerializer(evento, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"detail": "Evento no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verEvento(request, id):
    try:
        evento = Evento.objects.get(pk = id)
        serializer = listarEventoSerializer(evento, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Evento no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listarEventos(request):
    try:
        eventos = Evento.objects.all()
        serializer = listarEventoSerializer(eventos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Evento no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setImagenEvento(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk=id_usuario)
        evento = Evento.objects.get(pk= id)
        assert evento.creador == mago
        imagen = request.data['foto']
        evento.foto = imagen
        evento.save()
        serializer = crearEventoSerializer(evento, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Evento no valido"},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inscribirseEvento(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk=id_usuario)
        evento = Evento.objects.get(pk = id)
        assert evento.creador != mago
        assert mago not in evento.asistentes.all()
        evento.asistentes.add(mago)
        evento.save()
        serializer = listarEventoSerializer(evento, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Evento no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def desuscribirseEvento(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk=id_usuario)
        evento = Evento.objects.get(pk = id)
        assert evento.creador != mago
        assert mago in evento.asistentes.all()
        evento.asistentes.remove(mago)
        evento.save()
        serializer = listarEventoSerializer(evento, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Evento no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

