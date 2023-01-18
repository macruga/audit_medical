
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets


# Imports propios
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from core.models.soporte.origen_etnico import OrigenEtnicoModel
from core.serializers.soporte.origen_etnico import OrigenEtnicoSerializer


"""
@desc: Vista de consulta de origen_etnico
@params: modulo string - nombre del modulo app el cual debe estar registrado en la modelo  modulos con el mismo nombre

"""

class OrigenEtnicoView(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'OrigenEtnico'
    # Call classes for authorization model 
    permission_classes = (IsActive,)
    # permission_classes = ()
    queryset = OrigenEtnicoModel.objects.all()
    serializer_class = OrigenEtnicoSerializer

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )



    def list(self, request):
        query = OrigenEtnicoModel.objects.all()
        serializer = OrigenEtnicoSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_401_UNAUTHORIZED)        

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)