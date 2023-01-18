from rest_framework import serializers
# Importaciones propias
from core.models.soporte.escolaridad import EscolaridadModel



class EscolaridadSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= EscolaridadModel
        fields = '__all__'