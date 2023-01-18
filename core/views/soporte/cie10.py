from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions


from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from core.models.soporte.cie10 import Cie10Model
from core.serializers.soporte.cie10 import Cie10Serializer


class Cie10View(viewsets.ModelViewSet):
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'cie10'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = Cie10Model.objects.all()
    serializer_class = Cie10Serializer #  Default serializer

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request): # search according to parameter search passed in request
        search = request.GET.get('search', '')
        if search != '':
            # Peticion GET para retornar todos los registros de afiliados con estado activo
            query = Cie10Model.objects.filter(codigo__contains=search) | (
                Cie10Model.objects.filter(titulo__contains=search))
            serializer = Cie10Serializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)
       

    def create(self, request, *args, **kwargs):

        # Peticion POST para crear una cohorte a un afiliado
        serializer = Cie10Serializer(data=request.data)
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
        query = Cie10Model.objects.filter(codigo = pk).all()
        serializer = Cie10Serializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None): # pk = id de la aseguradora
        id_ = Cie10Model.objects.get(codigo_habilitacion=pk)
        serializer = Cie10Serializer(instance=id_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def destroy(self, request, pk=None):
        '''
        Borra un diagnostico cie10
        '''

        # TODO try para borrar, si da error es por integridad en la relacion, en ese caso enviar mensaje al usuario
        Cie10Model.objects.filter(codigo = pk ).delete()
        return Response(status=status.HTTP_200_OK)