from rest_framework import serializers
# Importaciones propias
from core.models.soporte.vulnerabilidad import VulnerabilidadModel



class VulnerabilidadSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= VulnerabilidadModel
        fields = '__all__'