from rest_framework import serializers
from core.models.soporte.cohorte import CohorteModel

class CohorteSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    # By defautl status is true
    status = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = CohorteModel
        fields = '__all__'