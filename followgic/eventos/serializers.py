from rest_framework import serializers, fields
from .models import *
from user.serializers import *
from user.models import Mago
from localizacion.serializers import crearLocalizacionSerializer

class crearEventoSerializer(serializers.ModelSerializer):
    localizacion = crearLocalizacionSerializer(many=False)
    class Meta:
        model = Evento
        fields = ['pk', 'titulo', 'tipo', 'privacidad', 'link_conferencia', 'descripcion', 'fecha_evento', 'hora_evento', 'aforo', 'foto', 'modalidades', 'comentarios', 'localizacion']

class listarEventoSerializer(serializers.ModelSerializer):
    localizacion = crearLocalizacionSerializer(many=False)
    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'tipo', 'privacidad', 'link_conferencia', 'descripcion', 'fecha_evento', 'hora_evento', 'aforo', 'foto', 'modalidades', 'comentarios', 'localizacion', 'asistentes']

class crearComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['pk', 'cuerpo', 'fecha', 'remitente']

class listarComentarioSerializer(serializers.ModelSerializer):
    remitente = listadoMagosSerializer(many=False)
    leidos = listadoMagosSerializer(many=True)
    class Meta:
        model = Comentario
        fields = ('pk', 'cuerpo', 'fecha', 'remitente', 'leidos')

class listarInvitacionesSerializer(serializers.ModelSerializer):
    evento= listarEventoSerializer(many = False)
    class Meta:
        model = Invitacion
        fields = ('pk','estado','fecha', 'evento', 'destinatario','token')