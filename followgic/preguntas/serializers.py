from rest_framework import serializers
from .models import Pregunta

class listarPreguntasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = ('pk','enunciado', 'primera_opcion', 'segunda_opcion', 'tercera_opcion', 'respuesta_correcta')