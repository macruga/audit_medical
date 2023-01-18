

from rest_framework import serializers


from estancias.models.estancia import EstanciaModel



class EstanciaSerializer(serializers.ModelSerializer):
     # Save owner
        
    active = serializers.HiddenField(
        default=True
        )
    estado = serializers.HiddenField(
        default=True
        )
   
    # When the stay is created the dx_actual is the dx_ingreso
    # dx_actual = serializers.HiddenField(
    #     default=validated_data['ips']
    #     )

    def create(self, validated_data):
        validated_data['dx_actual'] = validated_data['dx_ingreso']
        return super().create(validated_data)

    class Meta:
        model= EstanciaModel
        fields = '__all__'


class EstanciaUpdateSerializer(serializers.ModelSerializer):
     class Meta:
        model= EstanciaModel
        fields = ['fecha_ingreso', 'dx_ingreso', 
                'tipo_ingreso_id', 'origen_evento_id',
                'dx_actual']


class EgresoSerializer(serializers.ModelSerializer):
     class Meta:
        model= EstanciaModel
        fields = ['fecha_egreso', 'dx_egreso', 'condicion_alta_id']
