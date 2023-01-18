from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions


from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from censo.models.tipo_ingreso import TipoIngresoModel
from censo.serializers.tipo_ingreso import TipoIngresoSerializer


class TipoIngresoView(viewsets.ModelViewSet):
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'tipo-ingreso'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = TipoIngresoModel.objects.all()
    serializer_class = TipoIngresoSerializer #  Default serializer

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request): 
        # Peticion GET para retornar todos los registros de afiliados con estado activo
        query = TipoIngresoModel.objects.filter(active = 1).all()
        serializer = TipoIngresoSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       

    def create(self, request, *args, **kwargs):

        # Peticion POST para crear una cohorte a un afiliado
        serializer = TipoIngresoSerializer(data=request.data)
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
        query = TipoIngresoModel.objects.filter(id = pk).all()
        serializer = TipoIngresoSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None): # pk = id de la aseguradora
        id_ = TipoIngresoModel.objects.get(id=pk)
        serializer = TipoIngresoSerializer(instance=id_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def destroy(self, request, pk=None):
        '''
        Borra un tipo de ingreso
        '''

        # TODO try para borrar, si da error es por integridad en la relacion, en ese caso enviar mensaje al usuario
        TipoIngresoModel.objects.filter(id = pk ).delete()
        return Response(status=status.HTTP_200_OK)