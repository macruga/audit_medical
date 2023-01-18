
from rest_framework import serializers
from afiliados.models.afiliado import afiliadoModel

class NuevoAfiliadoSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    # estado_paciente = serializers.HiddenField(
    #     default='N'
    #     )

    class Meta:
        model = afiliadoModel
        fields = '__all__'


class ActualizarAfiliadoSerializer(serializers.ModelSerializer):   
    '''
        Serializador para defnir los campos que puden ser actualizados en el afiliado
    '''

    class Meta:
        model = afiliadoModel
        fields = ['tipo_identificacion','fecha_nacimiento','sexo','estado_civil','ocupacion_actual','discapacidad',
                  'codigo_departamento','codigo_municipio','codigo_zona_residencial','direccion','vulnerabilidad',
                  'pertenencia_etnica','grupo_poblacional','escolaridad','estado_paciente']


# TODO, validar si es necesario implementar un servicio de actualizacion solo para el estado