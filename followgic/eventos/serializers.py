from rest_framework import serializers, fields
from .models import *
from user.serializers import *
from user.models import Mago

class crearEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['pk', 'titulo', 'tipo', 'privacidad', 'link_conferencia', 'descripcion', 'fecha_evento', 'hora_evento', 'aforo', 'foto', 'modalidades', 'comentarios']

class listarEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class crearComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['pk', 'cuerpo', 'fecha', 'remitente']

class listarComentarioSerializer(serializers.ModelSerializer):
    remitente = listadoMagosSerializer(many=False)
    class Meta:
        model = Comentario
        fields = ('pk', 'cuerpo', 'fecha', 'remitente')

class listarInvitacionesSerializer(serializers.ModelSerializer):
    evento= listarEventoSerializer(many = False)
    class Meta:
        model = Invitacion
        fields = ('pk','estado','fecha', 'evento', 'destinatario','token')