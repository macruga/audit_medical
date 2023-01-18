from rest_framework import serializers

from infecciones.models.perfil_resistencia import PerfilResistenciaModel



class PerfilResistenciaSerializer(serializers.ModelSerializer):
   
    class Meta:
        model= PerfilResistenciaModel
        fields = '__all__'