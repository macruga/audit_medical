from rest_framework import serializers
# Importaciones propias
from core.models.soporte.municipios import MunicipioModel



class MunicipiosSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= MunicipioModel
        fields = '__all__'