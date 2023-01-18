from rest_framework import serializers

from core.models.soporte.servicios import ServiciosModel



class ServiciosSerializer(serializers.ModelSerializer):
   
    class Meta:
        model= ServiciosModel
        fields = '__all__'