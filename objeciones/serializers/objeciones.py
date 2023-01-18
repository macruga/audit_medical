from core.serializers.soporte.cums import CumsExpandSerializer
from core.serializers.usuarios import UserExpandSerializer
from rest_framework import serializers

from objeciones.models.objeciones import ObjecionModel
from objeciones.serializers.tipos_objeciones import TipoObjecionSerializer

class ObjecionSerializer(serializers.ModelSerializer):

#   cum_data = CumsExpandSerializer(source='cum', read_only=True)
  owner_data = UserExpandSerializer(source='owner', read_only=True)
  tipo_data = TipoObjecionSerializer(source='tipo_objecion', read_only=True)
#   usuario_solicitud_data = UserExpandSerializer(source='usuario_solicitud', read_only=True)
#   asesor_data = UserExpandSerializer(source='asesor', read_only=True)

  class Meta:
          model= ObjecionModel
          fields = "__all__"

          

