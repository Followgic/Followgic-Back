from rest_framework import serializers, fields
from .models import *

class crearEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['pk', 'titulo', 'tipo', 'descripcion', 'fecha_evento', 'aforo', 'foto']

class listarEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'