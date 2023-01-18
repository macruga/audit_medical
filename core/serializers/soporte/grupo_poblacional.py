from rest_framework import serializers
# Importaciones propias
from core.models.soporte.grupo_poblacional import GrupoPoblacionalModel



class GrupoPoblacionalSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= GrupoPoblacionalModel
        fields = '__all__'