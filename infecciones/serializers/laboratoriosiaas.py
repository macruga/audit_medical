from rest_framework import serializers

from infecciones.models.laboratoriosiaas import LaboratoriosIaasModel



class LabsIaasSerializer(serializers.ModelSerializer):
   
    class Meta:
        model= LaboratoriosIaasModel
        fields = '__all__'