from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from user.models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMisMensajesNoLeidos(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        mensajes = Mensaje.objects.filter(destinatario= mago, estado=0)
        serializer = listarMensajesSerializer(mensajes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "No hay mensajes nuevos"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMisMensajes(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        mensajes = Mensaje.objects.filter(destinatario= mago)
        serializer = listarMensajesSerializer(mensajes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "No tienes mensajes"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enviarMensaje(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        destinatario = Mago.objects.get(pk= id)
        assert destinatario != Mago.objects.get(pk= 1)
        assert destinatario != mago
        #No haya una peticion pendiente o una peticion aceptada (ya son amigos)
        mensaje = Mensaje()
        mensaje.estado = 0
        mensaje.fecha = date.today()
        mensaje.remitente = mago
        mensaje.destinatario = destinatario
        mensaje.save()
        serializer = listarMensajesSerializer(mensaje, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"detail": "Mensaje no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )
