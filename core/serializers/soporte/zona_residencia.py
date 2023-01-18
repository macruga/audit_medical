from rest_framework import serializers
# Importaciones propias
from core.models.soporte.zona_residencia import ZonaResidenciaModel



class ZonaResidenciaSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= ZonaResidenciaModel
        fields = '__all__'