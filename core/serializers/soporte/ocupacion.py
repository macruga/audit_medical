from rest_framework import serializers
# Importaciones propias
from core.models.soporte.ocupacion import OcupacionModel



class OcupacionSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= OcupacionModel
        fields = '__all__'