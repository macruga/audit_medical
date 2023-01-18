from rest_framework import serializers
# Importaciones propias
from core.models.soporte.origen_etnico import OrigenEtnicoModel



class OrigenEtnicoSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= OrigenEtnicoModel
        fields = '__all__'