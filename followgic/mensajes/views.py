from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from user.models import *
from datetime import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMisMensajesNoLeidos(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        res = []
        remitentes = []
        mensajes = Mensaje.objects.filter(destinatario= mago, estado=0)
        for m in mensajes:
            if m.remitente not in remitentes:
                res.append(m)
                remitentes.append(m.remitente)
        serializer = listarMensajesSerializer(res, many=True)
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
        res = []
        remitentes = []
        mensajes = Mensaje.objects.filter(destinatario= mago).order_by('-fecha')
        for m in mensajes:
            if m.remitente not in remitentes:
                res.append(m)
                remitentes.append(m.remitente)
        serializer = listarMensajesSerializer(res, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "No tienes mensajes"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enviarMensaje(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        destinatario = Mago.objects.get(pk= id)
        assert destinatario != Mago.objects.get(pk= 1)
        assert destinatario != mago
        mensaje = Mensaje()
        mensaje.estado = 0
        mensaje.fecha = datetime.now()
        mensaje.remitente = mago
        mensaje.destinatario = destinatario
        mensaje.cuerpo = request.data['cuerpo']
        mensaje.save()
        serializer = listarMensajesSerializer(mensaje, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"detail": "Mensaje no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verConversacion(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        mensaje = Mensaje.objects.get(pk= id)
        #Verificación de que el mensaje es del usuario actual
        assert mensaje.destinatario == mago
        mensajes_conversacion = Mensaje.objects.filter(remitente= mago, destinatario= mensaje.remitente).order_by('fecha') | Mensaje.objects.filter(remitente= mensaje.remitente, destinatario= mago).order_by('fecha')
        #El mensaje entrante del mago se marca como leido asi como los mensajes anteriores que tiene con dicho usuario si los hubiera
        if mensaje.estado == 0:
            mensaje.estado = 1
            mensaje.save()
            if Mensaje.objects.filter(destinatario=mago, remitente= mensaje.remitente, estado=0).count() != 0:
                mensajes = Mensaje.objects.filter(destinatario=mago, remitente= mensaje.remitente, estado=0)
                for m in mensajes:
                    m.estado = 1
                    m.save()
        serializer = listarMensajesSerializer(mensajes_conversacion, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "No tienes mensajes"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminarConversacion(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        mensaje = Mensaje.objects.get(pk= id)
        #Verificación de que el mensaje es del usuario actual
        assert mensaje.destinatario == mago
        mensajes_conversacion = Mensaje.objects.filter(remitente= mago, destinatario= mensaje.remitente) | Mensaje.objects.filter(remitente= mensaje.remitente, destinatario= mago)
        #Eliminar los mensajes de la conversacion
        for m in mensajes_conversacion:
            m.delete()
        return Response(
            {"detail": "Conversación eliminada correctamente"},
            status = status.HTTP_200_OK
        )
    except:
        return Response(
            {"detail": "La conversación no se ha podido eliminar"},
            status = status.HTTP_400_BAD_REQUEST
        )