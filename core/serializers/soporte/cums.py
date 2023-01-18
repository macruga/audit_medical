from rest_framework import serializers
from core.models.soporte.cums import CumsModel

class CumsSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = CumsModel
        fields = '__all__'


class CumsExpandSerializer(serializers.ModelSerializer):  

    class Meta:
        model = CumsModel
        fields = (
            "id","codigo","nombre_medicamento","expediente_cum","descripcion","registro_invima","principio_activo",
            "via_administracion","atc", "descripcion_atc","created","active")
                