from rest_framework import serializers
from user.models import Mago

class MagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mago
        fields = '__all__'