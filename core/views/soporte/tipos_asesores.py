from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets


# Imports propios
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from core.models.soporte.tipos_asesores import TiposAsesoresModel
from core.serializers.soporte.tipos_asesores import TiposAsesoresSerializer


"""
@desc: Vista de consulta de estado_civil
@params: modulo string - nombre del modulo app el cual debe estar registrado en la modelo  modulos con el mismo nombre

"""

class TiposAsesoresView(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'tipos_asesores'
    # Call classes for authorization model 
    permission_classes = (IsActive,)
    # permission_classes = ()
    queryset = TiposAsesoresModel.objects.all()
    serializer_class = TiposAsesoresSerializer

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )



    def list(self, request):
        query = TiposAsesoresModel.objects.all()
        serializer = TiposAsesoresSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # Peticion POST para crear una cohorte a un afiliado
        serializer = TiposAsesoresSerializer(data=request.data)
        try:
            request.data['owner'] = request.user.id          
        except:
            pass
        if serializer.is_valid():    
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # Petiion GET para retornar las aseguradoras por id
        query = TiposAsesoresModel.objects.filter(codigo_habilitacion = pk).all()
        serializer = TiposAsesoresSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        id_ = TiposAsesoresModel.objects.get(codigo_habilitacion=pk)
        serializer = TiposAsesoresSerializer(instance=id_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)