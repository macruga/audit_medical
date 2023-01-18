
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from core.models.soporte.cohorte import CohorteModel
from core.serializers.soporte.cohorte import CohorteSerializer


# Vista de consulta de usuarios
class CohorteView(viewsets.ModelViewSet):
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'Cohortes'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = CohorteModel.objects.all()
    serializer_class = CohorteSerializer


    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request): # pk = id del afiliado
        query = CohorteModel.objects.filter().all()
        serializer = CohorteSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        # Peticion POST para crear una cohorte a un afiliado
        serializer = CohorteSerializer(data=request.data)
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
        # Petiion GET para retornar las cohortes asignadas a un afiliado
        query = CohorteModel.objects.filter(id = pk).all()
        serializer = CohorteSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None): # pk = id de la cohorte
        data_update = request.data.dict()    
        serializer = CohorteSerializer(data=data_update)
        if serializer.is_valid():
            CohorteModel.objects.filter(id=pk).update(**data_update)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)