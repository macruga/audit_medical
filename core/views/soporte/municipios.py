
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets


# Imports propios
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from core.models.soporte.municipios import MunicipioModel
from core.serializers.soporte.municipios import MunicipiosSerializer


"""
@desc: Vista de consulta de municipios
@params: modulo string - nombre del modulo app el cual debe estar registrado en la modelo  modulos con el mismo nombre

"""

class MunicipiosView(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'Municipios'
    # Call classes for authorization model 
    permission_classes = (IsActive,)
    # permission_classes = ()
    queryset = MunicipioModel.objects.all()
    serializer_class = MunicipiosSerializer

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )



    def list(self, request):
        query = MunicipioModel.objects.all()
        serializer = MunicipiosSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_401_UNAUTHORIZED)        

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)