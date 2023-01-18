from rest_framework import serializers
# Importaciones propias
from core.models.soporte.tipo_documento import TipoDocumentoModel



class TipoDocumentoSerializer(serializers.ModelSerializer):
    # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model= TipoDocumentoModel
        fields = '__all__'