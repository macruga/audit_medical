from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions


from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from afiliados.models.afiliado_cohorte import CohorteAfiliadoModel
from afiliados.serializers.afiliado_cohorte import CohorteAfiliadoSerializer, ActualizarCohorteSerializer
from afiliados.custom_class.validators import cohortesRule

# Vista de consulta de usuarios
class CohorteAfiliadoView(viewsets.ModelViewSet):
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'Cohortes_Afiliados'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = CohorteAfiliadoModel.objects.all()
    serializer_class = CohorteAfiliadoSerializer


    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request, pk): # pk = id del afiliado
        query = CohorteAfiliadoModel.objects.filter(afiliado_id = pk).all()
        serializer = CohorteAfiliadoSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        # Peticion POST para crear una cohorte a un afiliado
        serializer = CohorteAfiliadoSerializer(data=request.data)
        try:
            request.data['owner'] = request.user.id          
        except:
            pass
        
        if serializer.is_valid(): 
            error, error_detail = cohortesRule(request.data).validate()# Raise error if any rule is broken
            if error:
                return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None): 
        # Petiion GET para retornar las cohortes asignadas a un afiliado
        query = CohorteAfiliadoModel.objects.filter(id = pk).all()
        serializer = CohorteAfiliadoSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None): # pk = id de la cohorte
        try:
            data_update = request.data.dict()  
        except:
            data_update = request.data
        serializer = ActualizarCohorteSerializer(data=data_update)
        if serializer.is_valid():
            # Call custom validators
            error, error_detail = cohortesRule(request.data).validate() # Raise error if any rule is broken
            if error:
                return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)

            CohorteAfiliadoModel.objects.filter(id=pk).update(**data_update)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

    def destroy(self, request, pk=None):
        '''
        Borra cohorte indicada al paciente
        '''
        CohorteAfiliadoModel.objects.filter(id = pk ).delete()
        return Response(status=status.HTTP_202_ACCEPTED)
