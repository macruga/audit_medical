
from rest_framework import serializers
from censo.models.tipo_habitacion import TipoHabitacionModel

class TipoHabitacionSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = TipoHabitacionModel
        fields = '__all__'