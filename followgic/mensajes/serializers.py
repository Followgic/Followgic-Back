from rest_framework import serializers
from .models import *

class listarMensajesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'