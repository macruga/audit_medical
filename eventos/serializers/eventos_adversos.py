from rest_framework import serializers
from eventos.models.eventos_adversos import EventosModel

class EventosSerializer(serializers.ModelSerializer):

  class Meta:
    model= EventosModel
    fields = "__all__"





