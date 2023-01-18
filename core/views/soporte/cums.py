from core.paginations import CustomPaginationAfiliados
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions


from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from core.models.soporte.cums import CumsModel
from core.serializers.soporte.cums import CumsExpandSerializer, CumsSerializer


class CumsView(viewsets.ModelViewSet):
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'cums'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = CumsModel.objects.all()
    serializer_class = CumsSerializer #  Default serializer
    pagination_class = CustomPaginationAfiliados

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request): # search according to parameter search passed in request
        search = request.GET.get('search', '')
        if search != '':
            # Peticion GET para retornar todos los registros de afiliados con estado activo
            queryset = CumsModel.objects.filter(active = 1) & \
                    ( CumsModel.objects.filter(codigo__contains=search) | \
                    CumsModel.objects.filter(nombre_medicamento__contains=search)) 

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = CumsExpandSerializer(page, many=True)
                result = self.get_paginated_response(serializer.data)
                data = result.data # pagination data
            else:
                serializer = CumsExpandSerializer(queryset, many=True)
                data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({
            'links': {
                'next': None,
                'previous': None
            },
            'total': 0,
            'page': 1, # can not set default = self.page
            'page_size': 10,
            'results': []}, status=status.HTTP_204_NO_CONTENT)
       

    def create(self, request, *args, **kwargs):

        # Peticion POST para crear una cohorte a un afiliado
        serializer = CumsSerializer(data=request.data)
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
        query = CumsModel.objects.filter(codigo = pk).all()
        serializer = CumsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None): # pk = id de la aseguradora
        id_ = CumsModel.objects.get(codigo_habilitacion=pk)
        serializer = CumsSerializer(instance=id_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def destroy(self, request, pk=None):
        '''
        Borra un diagnostico medicamento
        '''

        # TODO try para borrar, si da error es por integridad en la relacion, en ese caso enviar mensaje al usuario
        CumsModel.objects.filter(codigo = pk ).delete()
        return Response(status=status.HTTP_200_OK)