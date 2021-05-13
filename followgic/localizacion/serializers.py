from rest_framework import serializers, fields
from .models import *

class crearLocalizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizacion
        fields = ['pk', 'latitud', 'longitud', 'direccion']