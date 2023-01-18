from rest_framework import serializers
from afiliados.models.afiliacion import AfiliacionModel

class AfiliacionSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    status_afiliacion = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = AfiliacionModel
        fields = '__all__'

class ActualizarAfiliacionSerializer(serializers.ModelSerializer):   
    '''
        Serializador para definir los campos que puden ser actualizados
    '''

    class Meta:
        model = AfiliacionModel
        fields = ['regimen','fecha_afiliacion','fecha_vencimiento', 'status_afiliacion', 'aseguradora_id', 'ips_primaria']


class DetalleAfiliacionSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = AfiliacionModel
        fields = '__all__'