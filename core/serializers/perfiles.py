from rest_framework import serializers
# Importaciones propias
from core.models.perfiles import PerfilModel

class PerfilSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    active = serializers.HiddenField(
        default=True
        )
    def create(self, validated_data):
        ###### Se valida que no exista una regla para el mismo modulo y grupo ##############################################
        reglas_ = PerfilModel.objects.filter( modulo = validated_data['modulo'], group = validated_data['group'] ).values().last()
        print(reglas_) 
        if ( reglas_ is not None ):
            raise serializers.ValidationError('Ya existe una regla para el modulo en el grupo seleccionado')
        ######################################################################################################################

        profile_ = PerfilModel.objects.create(**validated_data)
        
        return profile_ # Retorna el perfil creado

    class Meta:
        model= PerfilModel
        fields = '__all__'