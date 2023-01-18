from rest_framework import serializers
# Importaciones propias
from core.models.soporte.estados_paciente import EstadosPacienteModel



class EstadosPacienteSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= EstadosPacienteModel
        fields = '__all__'