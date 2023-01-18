from rest_framework import serializers
from core.models.soporte.aseguradoras import AseguradorasModel

class AseguradorasSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = AseguradorasModel
        fields = '__all__'