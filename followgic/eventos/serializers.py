from rest_framework import serializers, fields
from .models import *

class crearEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['pk', 'titulo', 'tipo', 'link_conferencia', 'descripcion', 'fecha_evento', 'hora_evento', 'aforo', 'foto', 'modalidades']

class listarEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'