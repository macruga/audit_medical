from rest_framework import serializers

from infecciones.models.lugar_ocurrencia import LugarOcurrenciaModel



class LugarOcurrenciaSerializer(serializers.ModelSerializer):
   
    class Meta:
        model= LugarOcurrenciaModel
        fields = '__all__'