from rest_framework import serializers
# Importaciones propias
from core.models.soporte.estado_civil import EstadoCivilModel



class EstadoCivilSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= EstadoCivilModel
        fields = '__all__'