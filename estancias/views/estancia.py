from django.core.serializers import serialize
from core.paginations import CustomPaginationAfiliados
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

import json


# Import custom models
from estancias.models.estancia import EstanciaModel
# Import custom serializers
from estancias.serializers.estancia import EstanciaSerializer, EstanciaUpdateSerializer, \
                                           EgresoSerializer
# Permissions
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered   # Path to our custom permission
# validators
from core.validators import rangeDate
from estancias.validators import EstanciaValidators
from estancias.rules import EstanciaExisteRule


# Vista de la consulta
class EstanciaView(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'estancias'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = EstanciaModel.objects.all()

    # mapping serializer into the action, this permit select different serializers, accordin to the action
    serializer_classes = {
        'update': EstanciaUpdateSerializer,
        # ... other actions
    }
    default_serializer_class = EstanciaSerializer #  Default serializer
    pagination_class = CustomPaginationAfiliados
    
    # Override your get_serializer_class method.
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        '''
        Clase de vista busqueda de estancias activas
        @param: search: string, parametro de busqueda (
            Identificacion, fecha_ingreso , apellido, numero de historia clinica)
        @param: page: int, numero de pagina
        @param: limit: int, limite de registros por pagina
        @Output: json, lista de afiliados
        '''
        search = request.GET.get('search', '')
        ips_string = request.GET.get('ips', None)
        # Request data can have a list of ips, if not, get all ips
        # ips = request.data['ips'] if 'ips' in request.data else None
        # get array of ips
        ips = ips_string.split(',') if ips_string else None
        print(ips)
        if (ips and ips != [] and ips is not None):
            queryset = EstanciaModel.objects.filter(estado = True, codigo_ips_id__in=ips) & (
                EstanciaModel.objects.filter(afiliado_id__identificacion__contains=search) | 
                EstanciaModel.objects.filter(tipo_ingreso_id__description__contains=search)).order_by('-created')
            print(queryset.query)
        else:
            queryset = EstanciaModel.objects.filter(estado = True ) & (
                EstanciaModel.objects.filter(afiliado_id__identificacion__contains=search) | 
                EstanciaModel.objects.filter(tipo_ingreso_id__description__contains=search)).order_by('-created')

        query = queryset.values('id','fecha_ingreso', 'dx_ingreso', 'afiliado_id', 
                        'afiliado_id__identificacion', 'afiliado_id__nombres', 'afiliado_id__primer_apellido', 
                        'afiliado_id__segundo_apellido', 'codigo_ips_id', 'codigo_ips_id__ips', 'dx_actual__titulo',
                        'tipo_ingreso_id', 'origen_evento_id', 'origen_evento_id__description', 'dias_estancia', 'dx_actual',
                        'fecha_egreso', 'dx_egreso', 'tipo_ingreso_id', 'tipo_ingreso_id__description', 'estado')
        
        paginate = self.paginate_queryset(query)
        if paginate is not None:
            result = self.get_paginated_response(paginate)            
            data = result.data # pagination data
        else:
            data = paginate
        
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = EstanciaSerializer(data=request.data)
        # Assign owner from loggin user, if API fill it, get inmutable error, then pass
        try:
            request.data['owner'] = request.user.id            
        except:
            pass

        if serializer.is_valid():       
            validate = EstanciaValidators(data_estancia=request.data, serializer=serializer)   
            return validate.validateCreate()               
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        _rule1 = EstanciaExisteRule(pk).validate()
        if _rule1[0]:
            return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
        query = EstanciaModel.objects.get(id=pk)
        serializer = EstanciaSerializer(query)
        return Response(serializer.data)

    def update(self, request, pk=None):
        _rule1 = EstanciaExisteRule(pk).validate()
        if _rule1[0]:
            return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
        data_update = request.data.dict()
        serializer = EstanciaUpdateSerializer(data=data_update)
        if serializer.is_valid():
            validate = EstanciaValidators(data_estancia=request.data, serializer=serializer)   
            return validate.validateUpdate(pk) # Se pasa como parametro el id de la estancia a actualizar        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AnularEgresosView(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'anular_egreso'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = EstanciaModel.objects.all()
    serializer_class = EgresoSerializer
    
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        _rule1 = EstanciaExisteRule(pk).validate()
        if _rule1[0]:
            return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
        query = EstanciaModel.objects.get(id=pk)
        serializer = EstanciaSerializer(query)
        return Response(serializer.data)

    def update(self, request, pk=None):
        validate = EstanciaValidators(data_estancia=request.data)   
        return validate.anularEgresoValidator(pk)

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class EgresosView(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'egreso'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = EstanciaModel.objects.all()
    serializer_class = EgresoSerializer
    
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        _rule1 = EstanciaExisteRule(pk).validate()
        if _rule1[0]:
            return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
        query = EstanciaModel.objects.get(id=pk)
        serializer = EstanciaSerializer(query)
        return Response(serializer.data)

    def update(self, request, pk=None):
        _rule1 = EstanciaExisteRule(pk).validate()
        if _rule1[0]:
            return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
        data_update = request.data.dict()
        serializer = EgresoSerializer(data=data_update)
        if serializer.is_valid():
            validate = EstanciaValidators(data_estancia=request.data, serializer=serializer)   
            return validate.egresoValidator(pk) # Se pasa como parametro el id de la estancia a actualizar        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class WorklistView(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'estancias'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = EstanciaModel.objects.all()
    serializer_class = EstanciaSerializer
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        # Filtering consultas per user
        owner_id = request.user.id        
        query = EstanciaModel.objects.filter(dx_sindromatico = True).values('id', 'fecha_ingreso', 'dx_ingreso', 
        'tipo_ingreso_id__description',  'dx_actual','fecha_egreso','dx_egreso','dias_estancia','afiliado_id', # 'cohorte',
        'dx_sindromatico','dx_alto_riesgo','cohorte_seguimiento', 'estancia_prolongada') | \
             EstanciaModel.objects.filter(dx_alto_riesgo = True).values('id', 'fecha_ingreso', 'dx_ingreso',
        'tipo_ingreso_id__description',  'dx_actual','fecha_egreso','dx_egreso','dias_estancia','afiliado_id', #'cohorte',
        'dx_sindromatico','dx_alto_riesgo','cohorte_seguimiento', 'estancia_prolongada') | \
             EstanciaModel.objects.filter(estancia_prolongada = True).values('id', 'fecha_ingreso', 'dx_ingreso', 
        'tipo_ingreso_id__description',  'dx_actual','fecha_egreso','dx_egreso','dias_estancia','afiliado_id', # 'cohorte',
        'dx_sindromatico','dx_alto_riesgo','cohorte_seguimiento', 'estancia_prolongada') | \
             EstanciaModel.objects.filter(cohorte_seguimiento = True).values('id', 'fecha_ingreso', 'dx_ingreso', 
        'tipo_ingreso_id__description',  'dx_actual','fecha_egreso','dx_egreso','dias_estancia','afiliado_id', # 'cohorte',
        'dx_sindromatico','dx_alto_riesgo','cohorte_seguimiento', 'estancia_prolongada')
        # query = EstanciaModel.all()
        return Response(query, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        query = EstanciaModel.objects.get(id=pk)
        serializer = EstanciaSerializer(query)
        return Response(serializer.data)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)


  

class IpsEstanciasActivas(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'estancias'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = EstanciaModel.objects.all()
    serializer_class = EstanciaSerializer
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        try:
            # Get ips for active estancias 
            query = EstanciaModel.objects.filter(estado = True
            ).values('codigo_ips_id','codigo_ips_id__ips').distinct()
            return Response(query, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)


    