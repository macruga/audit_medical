from rest_framework import serializers
from afiliados.models.afiliado_cohorte import CohorteAfiliadoModel

class CohorteAfiliadoSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    # By defautl status is true
    # status = serializers.HiddenField(
    #     default=True
    #     )

    class Meta:
        model = CohorteAfiliadoModel
        fields = '__all__'

class ActualizarCohorteSerializer(serializers.ModelSerializer):   
    '''
        Serializador para definir los campos que puden ser actualizados
    '''

    class Meta:
        model = CohorteAfiliadoModel
        fields = ['cohorte_id','fecha_ingreso', 'fecha_retiro', 'status']