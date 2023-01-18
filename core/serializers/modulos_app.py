from rest_framework import serializers
# Importaciones propias
from core.models.modulos_app import ModuloApp



class ModuloAppSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= ModuloApp
        fields = '__all__'