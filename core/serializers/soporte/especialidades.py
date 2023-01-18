from rest_framework import serializers

from core.models.soporte.especialidades import EspecialidadesModel



class EspecialidadesSerializer(serializers.ModelSerializer):
   
    class Meta:
        model= EspecialidadesModel
        fields = '__all__'