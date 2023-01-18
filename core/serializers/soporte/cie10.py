from rest_framework import serializers
from core.models.soporte.cie10 import Cie10Model

class Cie10Serializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = Cie10Model
        fields = '__all__'