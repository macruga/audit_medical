from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions


from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from core.models.soporte.ips import IpsModel
from core.serializers.soporte.ips import IpsSerializer


class IpsView(viewsets.ModelViewSet):
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'Ips'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = IpsModel.objects.all()
    serializer_class = IpsSerializer #  Default serializer

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request): # search according to parameter search passed in request
        search = request.GET.get('search', '')
        if search != '':
            # Peticion GET para retornar todos los registros de afiliados con estado activo
            query = IpsModel.objects.filter(codigo_habilitacion__contains=search) | (
                IpsModel.objects.filter(ips__contains=search) |  
                IpsModel.objects.filter(nit__contains=search))
            serializer = IpsSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)
       

    def create(self, request, *args, **kwargs):

        # Peticion POST para crear una cohorte a un afiliado
        serializer = IpsSerializer(data=request.data)
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
        query = IpsModel.objects.filter(codigo_habilitacion = pk).all()
        serializer = IpsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None): # pk = id de la aseguradora
        id_ = IpsModel.objects.get(codigo_habilitacion=pk)
        serializer = IpsSerializer(instance=id_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def destroy(self, request, pk=None):
        '''
        Borra una seguradora
        '''

        # TODO try para borrar, si da error es por integridad en la relacion, en ese caso enviar mensaje al usuario
        IpsModel.objects.filter(codigo_habilitacion = pk ).delete()
        return Response(status=status.HTTP_200_OK)