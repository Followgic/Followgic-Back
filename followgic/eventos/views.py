from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from user.models import *
from datetime import *
from user.serializers import listadoMagosSerializer

def eliminarEventosCumplidos():
    #Eliminar los eventos que se han pasado de la fecha actual
    eventos = Evento.objects.all()
    fecha_actual = datetime.now().date()
    for evento in eventos:
        if(fecha_actual > evento.fecha_evento):
            evento.delete()

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
        evento.modalidades.set(request.data['modalidades'])

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
        #Comprobacion de eventos pasados de fecha
        eliminarEventosCumplidos()
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
        #Comprobacion de eventos pasados de fecha
        eliminarEventosCumplidos()
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
def cancelarInscripcionEvento(request, id):
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMagosInscritosPorEvento(request, id):
    try:
        evento = Evento.objects.get(pk = id)       
        asistentes = evento.asistentes.all()
        serializer = listadoMagosSerializer(asistentes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "No se han encontrado asistentes"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def eliminarAsistenteEvento(request, id_evento, id_usuario):
    try:
        id_creador = request.user.id
        mago = Mago.objects.get(pk= id_creador)
        evento = Evento.objects.get(pk = id_evento)
        assert evento.creador == mago
        usuario = Mago.objects.get(pk = id_usuario)
        assert usuario in evento.asistentes.all()
        asistentes = evento.asistentes.remove(usuario)
        serializer = listadoMagosSerializer(asistentes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "No se han encontrado asistentes"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editarEvento(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        evento = Evento.objects.get(pk= id)
        assert evento.creador == mago

        evento.titulo = request.data['titulo']
        if(evento.tipo == 0):
            evento.link_conferencia = request.data['link_conferencia']
        evento.descripcion = request.data['descripcion']
        evento.fecha_evento = request.data['fecha_evento']
        evento.hora_evento = request.data['hora_evento']
        evento.aforo = request.data['aforo']
        evento.save()
        evento.modalidades.set(request.data['modalidades'])

        serializer = crearEventoSerializer(evento, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"detail": "Evento no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminarEvento(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        evento = Evento.objects.get(pk= id)
        assert evento.creador == mago
        evento.delete()
        return Response(
            {"detail": "Evento eliminado correctamente"},
            status = status.HTTP_200_OK
        )
    except:
        return Response(
            {"detail": "Evento no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )