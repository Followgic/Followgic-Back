from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from user.models import *

class MagoProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Mago
        fields = ('username', 'email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'foto', 'modalidades', 'amigos')

class MagoCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Mago
        fields = ('username', 'password', 'email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'modalidades', 'amigos')

class listadoMagosSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Mago
        fields = ('nombre', 'nombre_artistico', 'foto')

class verPerfilMagoSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Mago
        fields = ('email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'modalidades', 'foto')

class FotoMagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mago
        fields = ['foto']

class ModalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidad
        fields = ['pk', 'nombre']

class amigosMagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mago
        fields = ['amigos']