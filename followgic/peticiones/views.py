from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from peticiones.models import *
from peticiones.serializers import *
from datetime import *
from user.models import *
from user.serializers import listadoMagosSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMisPeticionesPendientes(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        peticiones = Peticion.objects.filter(destinatario= mago, estado=0)
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
        assert destinatario != mago
        #No haya una peticion pendiente o una peticion aceptada (ya son amigos)
        if ((Peticion.objects.filter(remitente= mago, destinatario=destinatario, estado=0).count() == 0) 
        and (Peticion.objects.filter(remitente= destinatario, destinatario=mago, estado=0).count() == 0) 
        and (Peticion.objects.filter(remitente= mago, destinatario=destinatario, estado=1).count() == 0) 
        and (Peticion.objects.filter(remitente= destinatario, destinatario=mago, estado=1).count() == 0)):
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rechazarPeticionAmistad(request, id):
    try:
        #La peticion de amistad sea del usuario y que exista
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        peticion = Peticion.objects.get(id= id)
        assert peticion.destinatario == mago
        assert peticion.estado == 0
        #Eliminar la peticion de amistad
        peticion.delete()
        return Response(
            {"detail": "Petición de amistad rechazada"},
            status = status.HTTP_200_OK
        )
    except:
        return Response(
            {"detail": "La petición no se ha podido rechazar"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cancelarPeticionAmistad(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        peticion = Peticion.objects.get(pk= id)
        assert peticion.remitente == mago
        assert peticion.estado == 0
        peticion.delete()
        return Response(
            {"detail": "Petición de amistad cancelada"},
            status = status.HTTP_200_OK
        )
    except:
        return Response(
            {"detail": "La petición no se ha podido rechazar"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def aceptarPeticionAmistad(request, id):
    try:
        #La peticion de amistad sea del usuario y que exista
        id_usuario = request.user.id
        destinatario = Mago.objects.get(pk= id_usuario)
        peticion = Peticion.objects.get(id= id)
        remitente = Mago.objects.get(pk = peticion.remitente.id)
        assert peticion.destinatario == destinatario
        assert peticion.estado == 0
        destinatario.amigos.add(peticion.remitente)
        destinatario.save()
        remitente.amigos.add(peticion.destinatario)
        remitente.save()
        peticion.estado = 1
        peticion.save()
        return Response(
            {"detail": "Petición de amistad aceptada"},
            status = status.HTTP_200_OK
        )
    except:
        return Response(
            {"detail": "La petición no se ha podido aceptar"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def eliminarAmigo(request, id):
    try:
        #Comprueba que los usuarios sean amigos
        id_usuario = request.user.id
        mago_solicitante = Mago.objects.get(pk= id_usuario)
        mago_afectado = Mago.objects.get(pk= id)
        assert (Peticion.objects.filter(remitente= mago_solicitante, destinatario=mago_afectado, estado= 1).count() > 0) or (Peticion.objects.filter(remitente= mago_afectado, destinatario=mago_solicitante, estado= 1).count() > 0)
        mago_solicitante.amigos.remove(mago_afectado)
        mago_solicitante.save()
        mago_afectado.amigos.remove(mago_solicitante)
        mago_afectado.save()
        #Se elimina la peticion de amistad aceptada 
        if (Peticion.objects.filter(remitente= mago_solicitante, destinatario=mago_afectado, estado= 1).count() > 0):
            Peticion.objects.get(remitente= mago_solicitante, destinatario=mago_afectado, estado= 1).delete()
            return Response(
                {"detail": "Mago eliminado de tu lista de amigos"},
                status = status.HTTP_200_OK
            )
        elif (Peticion.objects.filter(remitente= mago_afectado, destinatario=mago_solicitante, estado= 1).count() > 0):
            Peticion.objects.get(remitente= mago_afectado, destinatario=mago_solicitante, estado= 1).delete()
            return Response(
                {"detail": "Mago eliminado de tu lista de amigos"},
                status = status.HTTP_200_OK
            )
    except:
        return Response(
            {"detail": "No se ha podido eliminar este mago de tu lista de amigos"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuariosConPeticionesPendientes(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk=id_usuario)
        usuarios = []
        peticiones = Peticion.objects.filter(remitente= mago, estado=0)
        for p in peticiones:
            usuarios.append(p.destinatario)
        peticiones_entrantes = Peticion.objects.filter(destinatario=mago, estado=0)
        for p in peticiones_entrantes:
            usuarios.append(p.remitente)
        serializer = listadoMagosSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"detail": "Fallo al obtener las peticiones"},
            status = status.HTTP_400_BAD_REQUEST
        )

