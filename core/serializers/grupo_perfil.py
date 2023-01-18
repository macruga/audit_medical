from rest_framework import serializers
# Importaciones propias
from core.models.grupo_perfil import GrupoPerfil



class GroupPerfilSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= GrupoPerfil
        fields = '__all__'