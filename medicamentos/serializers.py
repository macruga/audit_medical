from core.serializers.soporte.cums import CumsExpandSerializer
from core.serializers.usuarios import UserExpandSerializer
from objeciones.models.objeciones import ObjecionModel
from objeciones.serializers.objeciones import ObjecionSerializer
from rest_framework import serializers

from medicamentos.models import MedicamentoModel
# from objeciones.models.objeciones import ObjecionModel

class MedicamentoSerializer(serializers.ModelSerializer):

  cum_data = CumsExpandSerializer(source='cum', read_only=True)
  owner_data = UserExpandSerializer(source='owner', read_only=True)
  auditor_data = UserExpandSerializer(source='auditor', read_only=True)
  usuario_solicitud_data = UserExpandSerializer(source='usuario_solicitud', read_only=True)
  asesor_data = UserExpandSerializer(source='asesor', read_only=True)


  def to_representation(self, instance): 
        '''
        Send objecion_data representation

        '''     
        
        data = super().to_representation(instance) 
        if data['objecion_id'] is not None:
                data['objecion_data'] = ObjecionModel.objects.filter(
                        id= int(instance.objecion_id)).values(
                                'id','estancia_id','cums','cups','medicamento_id',
                                'tipo','cantidad','valor','fecha_objecion','nota_objecion',
                                'created','owner__username','owner__first_name',
                                'owner__last_name','owner__email'
                        ).last()
        else:
                data['objecion_data'] = None
        return data

  class Meta:
          model= MedicamentoModel
          fields = "__all__"


class PertinenciaSerializer(serializers.ModelSerializer):  
     class Meta:
        model= MedicamentoModel
        fields = ['pertinencia', 'fecha_pertinencia', 'observacion_concurrente','auditor']


class AsesoriaSerializer(serializers.ModelSerializer):
     class Meta:
        model= MedicamentoModel
        fields = ['solicitud_asesoria','especialidad_asesoria', 'fecha_solicitud', 'motivo_revision_asesor','usuario_solicitud']


class AsesorSerializer(serializers.ModelSerializer):  
     class Meta:
        model= MedicamentoModel
        fields = ['nota_asesor','solicitud_asesoria', 'fecha_asesoria', 'asesor']