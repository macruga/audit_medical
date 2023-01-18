from rest_framework import serializers
# Importaciones propias
from core.models.soporte.tipos_asesores import TiposAsesoresModel



class TiposAsesoresSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= TiposAsesoresModel
        fields = '__all__'