from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from user.models import *

class MagoProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Mago
        fields = ('username', 'email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'foto', 'modalidades')

class MagoCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Mago
        fields = ('username', 'password', 'email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'modalidades')

class FotoMagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mago
        fields = ['foto']

class ModalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidad
        fields = ['pk', 'nombre']