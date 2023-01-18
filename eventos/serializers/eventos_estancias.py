from core.serializers.usuarios import UserExpandSerializer
from eventos.models.eventos_estancias import EventosEstanciaModel
from eventos.serializers.eventos_adversos import EventosSerializer

from rest_framework import serializers

class EventosEstanciaSerializer(serializers.ModelSerializer):

  evento_data = EventosSerializer(source='evento_id', read_only=True)
  owner_data = UserExpandSerializer(source='owner', read_only=True)


  class Meta:
          model= EventosEstanciaModel
          fields = "__all__"

