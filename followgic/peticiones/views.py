from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from peticiones.models import *
from peticiones.serializers import *
from datetime import *
from user.models import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMisPeticionesPendientes(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        peticiones = Peticion.objects.filter(destinatario= mago)
        serializer = listarPeticionesSerializer(peticiones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Peticiones no encontradas"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def crearPeticionAmistad(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        destinatario = Mago.objects.get(pk= id)
        assert destinatario != Mago.objects.get(pk= 1)
        if (Peticion.objects.filter(remitente= mago, destinatario=destinatario).count() == 0):
            peticion = Peticion()
            peticion.estado = 0
            peticion.fecha = date.today()
            peticion.remitente = mago
            peticion.destinatario = destinatario
            peticion.save()
            serializer = listarPeticionesSerializer(peticion, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
            {"detail": "Petición ya existente"},
            status = status.HTTP_400_BAD_REQUEST
        ) 
    except:
        return Response(
            {"detail": "Petición no valida"},
            status = status.HTTP_400_BAD_REQUEST
        )