from rest_framework import serializers
# Importaciones propias
from core.models.soporte.cif import CifModel



class CifSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )

    class Meta:
        model= CifModel
        fields = '__all__'