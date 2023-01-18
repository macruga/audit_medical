from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions


from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from core.paginations import CustomPaginationAfiliados
from afiliados.models.afiliado import afiliadoModel
from afiliados.serializers.afiliado import NuevoAfiliadoSerializer, ActualizarAfiliadoSerializer
from afiliados.custom_class.creacionAfiliados import EstPacienteNuevo


# Vista de consulta de afiliados
class AfiliadoView(viewsets.ModelViewSet):
   
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'Afiliado'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = afiliadoModel.objects.all()

    # mapping serializer into the action, this permit select different serializers, accordin to the action
    serializer_classes = {
        'update': ActualizarAfiliadoSerializer,
        # ... other actions
    }
    default_serializer_class = NuevoAfiliadoSerializer #  Default serializer

    # Override your get_serializer_class method.
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    serializer_class = NuevoAfiliadoSerializer
    pagination_class = CustomPaginationAfiliados


    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        '''
        Clase de vista busqueda de afiliados
        @param: search: string, parametro de busqueda (Identificacion, nombre, apellido, numero de historia clinica)
        @param: page: int, numero de pagina
        @param: limit: int, limite de registros por pagina
        @Output: json, lista de afiliados
        '''
        search = request.GET.get('search', '')
        # Peticion GET para retornar todos los registros de afiliados con estado activo
        query = afiliadoModel.objects.filter(active = True) & (
            
            afiliadoModel.objects.filter(tipo_identificacion__codigo__contains=search) |  
            afiliadoModel.objects.filter(identificacion__contains=search) |            
            afiliadoModel.objects.filter(nombres__contains=search) |
            afiliadoModel.objects.filter(primer_apellido__contains=search) |
            afiliadoModel.objects.filter(segundo_apellido__contains=search) 
            ).order_by('-created')

        page = self.paginate_queryset(query)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = self.get_serializer(query, many=True)
            data = serializer.data
    
     
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        
        # Peticion POST para crear un afiliado
        serializer = NuevoAfiliadoSerializer(data=request.data)
        # print(request.data)
        try:
            request.data['owner'] = request.user.id          
        except:
            pass
        
        if serializer.is_valid(): 
            
            #Se valida si el paciente no existe para crear un nuevo registro
            validate_pac =  EstPacienteNuevo(request.data['identificacion'])  
            resp = validate_pac.validate()
            if not resp['status']:    
                serializer.save()
                # TODO Crear la nueva estancia
                # TODO Definir si se crea de forma automatica, tabla configuraciones
                # Cambia el estado del paciente
                afiliadoModel.objects.filter(identificacion = request.data['identificacion']).update(
                    estado_paciente = 'I'
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif resp['estancia'] != 0:
                return Response(resp, status=status.HTTP_200_OK)
            else: 
                return Response(resp, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        # Petiion GET para retornar un afiliado en especifico
        query = afiliadoModel.objects.filter(id = pk).all()
        serializer = NuevoAfiliadoSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        '''
            En esta vista se obtienen los datos desde el modelo completo para dar la opcion al usuario de enviar solo 
            el parametro que desea modificar, el metodo trae todos los datos actuales del objeto,
            y crea un diccionario con los llaves de los datos que se envien en el request, los demas los sin cambios
        '''
        # print(request.data)
        # # afiliado = dict(afiliadoModel.objects.filter(id = pk).values().last())
        # query = afiliadoModel.objects.filter(id = pk).all()
        # # Get cohortes
        # cohortes_list = list(request.data['cohorte'])
        # print(cohortes_list)
        # # Pass query data to serializer
        # afiliado_serializado = NuevoAfiliadoSerializer(query, many=True)
        # # Save serialized data
        # afiliado = dict(afiliado_serializado.data[0])
        # print(afiliado)
        # #Get serializer fields
        # keys = ActualizarAfiliadoSerializer.Meta.fields
        # # Update data according to the request 
        # data_update = {} # Pass only data in request and fields must be in seriaizer stament
        # for key in keys:
        #         data_update[key] = request.data.get(key, afiliado[key])
        # # Update cohortes
        # data_update['cohorte'] = cohortes_list
        # print(data_update)
        # # Serialize data using update model 
        
        # serializer = ActualizarAfiliadoSerializer(data=data_update)

        # if serializer.is_valid():
        #     afiliadoModel.objects.filter(id=pk).update(**data_update)
        #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data_update = request.data
      
        serializer = ActualizarAfiliadoSerializer(data=data_update)
        if serializer.is_valid():
            afiliadoModel.objects.filter(id=pk).update(**data_update)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

    def destroy(self, request):
        # TODO: definir si se elimina el registro o se cambia el estado
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class AfiliadosIngresadosView(viewsets.ModelViewSet):
    '''
        Clase de vista para retornar solo los pacientes ingresados en el sistema (estancia activa)

    '''
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'Afiliado'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = afiliadoModel.objects.all()
    serializer_class = NuevoAfiliadoSerializer

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        # Petiion GET para retornar todos los registros de afiliados con estado activo
        query = afiliadoModel.objects.filter(active = True, estado_paciente = 'I').all()
        serializer = NuevoAfiliadoSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AfiliadoSearchView(viewsets.ModelViewSet):
   
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'Afiliado'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = afiliadoModel.objects.all()
    serializer_class = NuevoAfiliadoSerializer


    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        '''
        Clase de vista busqueda de afiliados
        @param: search: string, parametro de busqueda (Identificacion)
        @Output: json, lista de afiliados
        '''
        search = request.GET.get('search', '')
        # Peticion GET para retornar todos los registros de afiliados con estado activo
        query = afiliadoModel.objects.filter(active = True) & (  
            afiliadoModel.objects.filter(identificacion__contains=search)
            )

        serializer = self.get_serializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


