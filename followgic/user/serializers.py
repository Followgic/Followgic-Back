from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from user.models import *
from localizacion.serializers import crearLocalizacionSerializer

class MagoProfileSerializer(UserSerializer):
    localizacion = crearLocalizacionSerializer(many=False)
    class Meta(UserSerializer.Meta):
        model = Mago
        fields = ('pk', 'username', 'email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'foto', 'modalidades', 'amigos', 'localizacion')

class MagoCreateSerializer(UserCreateSerializer):
    localizacion = crearLocalizacionSerializer(many=False)
    class Meta(UserCreateSerializer.Meta):
        model = Mago
        fields = ('pk', 'username', 'password', 'email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'modalidades', 'amigos', 'localizacion')

class listadoMagosSerializer(UserCreateSerializer):
    localizacion = crearLocalizacionSerializer(many=False)
    class Meta(UserCreateSerializer.Meta):
        model = Mago
        fields = ('pk','nombre', 'nombre_artistico', 'foto', 'modalidades', 'localizacion')

class verPerfilMagoSerializer(UserCreateSerializer):
    localizacion = crearLocalizacionSerializer(many=False)
    class Meta(UserCreateSerializer.Meta):
        model = Mago
        fields = ('email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'modalidades', 'foto', 'localizacion')

class FotoMagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mago
        fields = ['foto']

class ModalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidad
        fields = ['pk', 'nombre']

class createModalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidad
        fields = ['pk', 'nombre']

class amigosMagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mago
        fields = ['amigos']