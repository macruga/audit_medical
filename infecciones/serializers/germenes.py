from rest_framework import serializers

from infecciones.models.germenes import GermenModel



class GermenSerializer(serializers.ModelSerializer):
   
    class Meta:
        model= GermenModel
        fields = '__all__'