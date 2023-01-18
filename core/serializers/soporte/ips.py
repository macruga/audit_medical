from rest_framework import serializers
from core.models.soporte.ips import IpsModel

class IpsSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = IpsModel
        fields = '__all__'