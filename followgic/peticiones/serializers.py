from rest_framework import serializers
from peticiones.models import *

class listarPeticionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peticion
        fields = '__all__'

class idPeticionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peticion
        fields = ['pk']
