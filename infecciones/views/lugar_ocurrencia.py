from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from infecciones.models.lugar_ocurrencia import LugarOcurrenciaModel
from infecciones.serializers.lugar_ocurrencia import LugarOcurrenciaSerializer


class LugarOcurrenciasView(viewsets.ModelViewSet):
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'lugarocurrencia'
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,) 
    queryset = LugarOcurrenciaModel.objects.all()
    serializer_class = LugarOcurrenciaSerializer

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    # Peticion GET
    def list(self, request): 
        # Peticion GET para retornar todos los registros de afiliados con estado activo
        query = LugarOcurrenciaModel.objects.filter(active = 1).all()
        serializer = LugarOcurrenciaSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       
    # Peticion POST
    def create(self, request, *args, **kwargs):

        # Peticion POST para crear una cohorte a un afiliado
        serializer = LugarOcurrenciaSerializer(data=request.data)
        try:
            request.data['owner'] = request.user.id          
        except:
            pass
        if serializer.is_valid():    
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Peticion GET, para retornar un registro especifico
    def retrieve(self, request, pk=None): 
        query = LugarOcurrenciaModel.objects.filter(id = pk).all()
        serializer = LugarOcurrenciaSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Peticion PUT
    def update(self, request, pk=None): # pk = id de la aseguradora
        id_ = LugarOcurrenciaModel.objects.get(id=pk)
        serializer = LugarOcurrenciaSerializer(instance=id_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    # Peticion DELETE
    def destroy(self, request, pk=None):
        '''
        Borra un servicio de estancia
        '''

        # TODO try para borrar, si da error es por integridad en la relacion, en ese caso enviar mensaje al usuario
        LugarOcurrenciaModel.objects.filter(id = pk ).delete()
        return Response(status=status.HTTP_200_OK)
