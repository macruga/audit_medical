from rest_framework import serializers
# Importaciones propias
from core.models.soporte.departamentos import DepartamentoModel



class DepartamentosSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= DepartamentoModel
        fields = '__all__'