from rest_framework import serializers
from censo.models.origen_evento import OrigenEventoModel

class OrigenEventoSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = OrigenEventoModel
        fields = '__all__'