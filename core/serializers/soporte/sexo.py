from rest_framework import serializers
# Importaciones propias
from core.models.soporte.sexo import SexoModel



class SexoSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= SexoModel
        fields = '__all__'