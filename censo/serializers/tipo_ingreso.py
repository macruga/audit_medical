from rest_framework import serializers
from censo.models.tipo_ingreso import TipoIngresoModel

class TipoIngresoSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = TipoIngresoModel
        fields = '__all__'