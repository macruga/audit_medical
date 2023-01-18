from rest_framework import serializers
from core.models.soporte.regimen import RegimenModel

class RegimenSerializer(serializers.ModelSerializer):   
    # Fill default parameters

    active = serializers.HiddenField(
        default=True
        )

    class Meta:
        model = RegimenModel
        fields = '__all__'