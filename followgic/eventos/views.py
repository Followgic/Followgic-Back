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
from cryptography.fernet import Fernet
from mensajes.views import sonAmigos

def eliminarEventosCumplidos():
    #Eliminar los eventos que se han pasado de la fecha actual
    eventos = Evento.objects.all()
    fecha_actual = datetime.now().date()
    for evento in eventos:
        if(fecha_actual > evento.fecha_evento):
            print('Estamos en el delete')
            if(evento.comentarios.all().count() > 0):
                evento.comentarios.all().delete()
            if(Invitacion.objects.filter(evento=evento).count() > 0):
                Invitacion.objects.filter(evento=evento).delete()
            evento.delete()

def eliminarInvitacionesConTokenCumplidos():
    #Eliminar las invitaciones que el token haya expirado
    invitaciones = Invitacion.objects.all()
    fecha_actual = datetime.now().date()
    for invitacion in invitaciones:
        fecha_expiracion = invitacion.fecha + timedelta(days=1)
        if(fecha_actual > fecha_expiracion):
            invitacion.delete()

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
        evento.privacidad = request.data['privacidad']
        #Si el evento es privado se genera token y se guarda en BD
        if(request.data['privacidad'] == 1):
            token = Fernet.generate_key()
            evento.token = token
        evento.descripcion = request.data['descripcion']
        evento.fecha_creacion = datetime.now()
        evento.fecha_evento = request.data['fecha_evento']
        evento.hora_evento = request.data['hora_evento']
        evento.aforo = request.data['aforo']
        if(request.data['foto'] != ''):
            evento.foto = request.data['foto']
        evento.creador = mago
        #Crear el comentario inicial del evento
        comentario = Comentario()
        comentario.fecha = datetime.now()
        comentario.remitente = mago
        if(request.data['comentario'] == ''):
            comentario.cuerpo = '¡Bienvenido a ' + request.data['titulo'] + '!'
        else:
            comentario.cuerpo = request.data['comentario']
        comentario.save()
        evento.save()
        evento.modalidades.set(request.data['modalidades'])
        evento.usuarios_activos.add(mago)
        evento.comentarios.add(comentario)
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
        #Comprobacion de eventos pasados de fecha
        eliminarEventosCumplidos()
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
        #Comprobacion de eventos pasados de fecha
        eliminarEventosCumplidos()
        eventos = Evento.objects.filter(privacidad=0)
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
        assert mago not in evento.usuarios_activos.all()
        assert evento.privacidad == 0
        #Validar si tiene invitacion privada
        assert evento.privacidad == 0
        assert Invitacion.objects.filter(evento= evento, destinatario=mago).count() == 0
        evento.asistentes.add(mago)
        evento.usuarios_activos.add(mago)
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
        assert mago in evento.usuarios_activos.all()
        #Validar si hay invitacion privada
        if(Invitacion.objects.filter(evento= evento, destinatario=mago).count() > 0):
            Invitacion.objects.get(evento=evento, destinatario=mago).delete()
        evento.asistentes.remove(mago)
        evento.usuarios_activos.remove(mago)
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
        evento.usuarios_activos.remove(usuario)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def silenciarEvento(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        evento = Evento.objects.get(pk= id)
        assert evento.creador != mago
        assert mago in evento.asistentes.all()
        assert mago in evento.usuarios_activos.all()
        evento.usuarios_activos.remove(mago)
        evento.save()
        return Response(
            {"detail": "Evento silenciado correctamente"},
            status = status.HTTP_200_OK
        )
    except:
        return Response(
            {"detail": "Evento no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def habilitarMensajesEvento(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        evento = Evento.objects.get(pk= id)
        assert evento.creador != mago
        assert mago in evento.asistentes.all()
        assert mago not in evento.usuarios_activos.all()
        evento.usuarios_activos.add(mago)
        evento.save()
        return Response(
            {"detail": "Habilitadas los mensajes de este evento correctamente"},
            status = status.HTTP_200_OK
        )
    except:
        return Response(
            {"detail": "Evento no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verEventosCreadosPorMi(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        eventos = Evento.objects.filter(creador= mago)
        serializer = listarEventoSerializer(eventos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "No se han encontrado eventos creados por ti"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verEventosSubscritos(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        eventos = []
        for evento in Evento.objects.all():
            if(mago in evento.asistentes.all()):
                eventos.append(evento)
        serializer = listarEventoSerializer(eventos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "No se han encontrado eventos"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enviarComentario(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        evento = Evento.objects.get(pk= id)
        assert mago in evento.asistentes.all() or mago == evento.creador
        assert mago in evento.usuarios_activos.all()

        comentario = Comentario()
        comentario.fecha = datetime.now()
        comentario.remitente = mago
        comentario.cuerpo = request.data['cuerpo']
        comentario.save()
        evento.comentarios.add(comentario)
        serializer = crearComentarioSerializer(comentario, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"detail": "Comentario no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verUltimoComentarioEvento(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        evento = Evento.objects.get(pk= id)
        assert mago in evento.asistentes.all() or mago == evento.creador
        assert mago in evento.usuarios_activos.all()
        comentario = evento.comentarios.all().reverse()[0]
        serializer = listarComentarioSerializer(comentario, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"detail": "Comentario no valido"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verComentariosEvento(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        evento = Evento.objects.get(pk= id)
        assert mago in evento.asistentes.all() or mago == evento.creador
        assert mago in evento.usuarios_activos.all()
        comentarios = evento.comentarios.all()
        serializer = listarComentarioSerializer(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"detail": "No se han encontrado comentarios"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminarComentario(request, id):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        comentario = Comentario.objects.get(pk= id)
        assert comentario.remitente == mago
        comentario.delete()
        return Response(
            {"detail": "Comentario borrado"},
            status = status.HTTP_200_OK
        )
    except:
        return Response(
            {"detail": "El comentario no se ha podido borrar"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMisInvitaciones(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        eliminarInvitacionesConTokenCumplidos()
        invitaciones = Invitacion.objects.filter(destinatario= mago, estado=0)
        serializer = listarInvitacionesSerializer(invitaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "No se han encontrado invitaciones"},
            status = status.HTTP_204_NO_CONTENT
        )

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def codigoInvitacion(request, cadena=None):
    try:
        #GENERAR CODIGO DE INVITACION
        if(request.method == 'GET'):
            #usuario creador del evento
            id_usuario_actual = request.user.id
            usuario = Mago.objects.get(pk= id_usuario_actual)
            id_evento = cadena.split("|")[0]
            id_usuario = cadena.split("|")[1]
            evento = Evento.objects.get(pk= id_evento)
            invitado = Mago.objects.get(pk= id_usuario)
            #Validaciones
            assert evento.privacidad == 1
            assert usuario == evento.creador
            assert invitado not in evento.asistentes.all()
            assert sonAmigos(usuario, int(id_usuario)) == True
            assert Invitacion.objects.filter(evento=evento, destinatario=invitado).count() == 0
            #Generador de token
            f = Fernet(Evento.objects.get(pk= id_evento).token.split("'")[1].encode())
            token_encriptado = f.encrypt(cadena.encode())
            #Se crea la peticion de invitacion al evento privado AQUI
            invitacion = Invitacion()
            invitacion.estado = 0
            invitacion.fecha = datetime.now()
            invitacion.token = token_encriptado
            invitacion.evento = evento
            invitacion.destinatario = invitado
            invitacion.save()
            serializer = listarInvitacionesSerializer(invitacion, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #ACEPTAR CODIGO DE INVITACION
        if(request.method == 'POST'):
            id_usuario = request.user.id
            usuario = Mago.objects.get(pk= id_usuario)
            eliminarInvitacionesConTokenCumplidos()
            invitacion = Invitacion.objects.get(pk= int(cadena))
            evento = Evento.objects.get(pk= invitacion.evento.pk)
            f = Fernet(str(evento.token).split("'")[1])
            mensaje_descifrado = f.decrypt(str(invitacion.token).split("'")[1].encode()).decode()
            assert evento.privacidad == 1
            assert usuario == invitacion.destinatario and usuario.pk == int(mensaje_descifrado.split('|')[1])
            assert invitacion.estado == 0
            assert invitacion.evento.pk == int(mensaje_descifrado.split('|')[0])
            assert usuario not in evento.asistentes.all()
            assert usuario not in evento.usuarios_activos.all()
            invitacion.estado = 1
            evento.asistentes.add(usuario)
            evento.usuarios_activos.add(usuario)
            invitacion.save()
            serializer = listarInvitacionesSerializer(invitacion, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #RECHAZAR CODIGO DE INVITACION (METODO DELETE)
        if(request.method == 'DELETE'):
            id_usuario = request.user.id
            usuario = Mago.objects.get(pk= id_usuario)
            eliminarInvitacionesConTokenCumplidos()
            invitacion = Invitacion.objects.get(pk= int(cadena))
            evento = Evento.objects.get(pk= invitacion.evento.pk)
            f = Fernet(str(evento.token).split("'")[1])
            mensaje_descifrado = f.decrypt(str(invitacion.token).split("'")[1].encode()).decode()
            assert evento.privacidad == 1
            assert usuario == invitacion.destinatario and usuario.pk == int(mensaje_descifrado.split('|')[1])
            assert invitacion.estado == 0
            assert invitacion.evento.pk == int(mensaje_descifrado.split('|')[0])
            assert usuario not in evento.asistentes.all()
            assert usuario not in evento.usuarios_activos.all()
            invitacion.delete()
            return Response({"detail": "Invitacion rechazada"}, status = status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Evento no encontrado"},
            status = status.HTTP_400_BAD_REQUEST
        )

