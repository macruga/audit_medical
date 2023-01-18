# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from eventos.models.eventos_adversos import EventosModel
from eventos.serializers.eventos_adversos import EventosSerializer
# Permissions
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered   # Path to our custom permission

class EventosView(viewsets.ModelViewSet):
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'eventos'
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,) 
    queryset = EventosModel.objects.all()
    serializer_class = EventosSerializer

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    # Peticion GET
    def list(self, request): 
        # Peticion GET para retornar todos los registros de afiliados con estado activo
        query = EventosModel.objects.filter(active = 1).all()
        serializer = EventosSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       
    # Peticion POST
    def create(self, request, *args, **kwargs):

        # Peticion POST para crear una cohorte a un afiliado
        serializer = EventosSerializer(data=request.data)
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
        query = EventosModel.objects.filter(id = pk).all()
        serializer = EventosSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Peticion PUT
    def update(self, request, pk=None): # pk = id de la aseguradora
        id_ = EventosModel.objects.get(id=pk)
        serializer = EventosSerializer(instance=id_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    # Peticion DELETE
    def destroy(self, request, pk=None):
        '''
        Borra un evento adverso
        '''

        # TODO try para borrar, si da error es por integridad en la relacion, en ese caso enviar mensaje al usuario
        EventosModel.objects.filter(id = pk ).delete()
        return Response(status=status.HTTP_200_OK)






