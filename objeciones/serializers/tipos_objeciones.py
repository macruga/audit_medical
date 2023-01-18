from core.serializers.soporte.cums import CumsExpandSerializer
from core.serializers.usuarios import UserExpandSerializer
from rest_framework import serializers

from objeciones.models.tipos_objeciones import TipoObjecionModel

class TipoObjecionSerializer(serializers.ModelSerializer):

#   cum_data = CumsExpandSerializer(source='cum', read_only=True)
#   owner_data = UserExpandSerializer(source='owner', read_only=True)
#   auditor_data = UserExpandSerializer(source='auditor', read_only=True)
#   usuario_solicitud_data = UserExpandSerializer(source='usuario_solicitud', read_only=True)
#   asesor_data = UserExpandSerializer(source='asesor', read_only=True)

  class Meta:
          model= TipoObjecionModel
          fields = "__all__"

