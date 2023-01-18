from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions


from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from afiliados.models.afiliacion import AfiliacionModel
from afiliados.serializers.afiliacion import AfiliacionSerializer, ActualizarAfiliacionSerializer, DetalleAfiliacionSerializer
from afiliados.rules import AfiliacionMayorVencimientoRule

# Vista de consulta de usuarios
class AfiliacionView(viewsets.ModelViewSet):
    # TODO variable de entorno para declarar los modulos
    # All views must contain a model  name for the permissions are efective:
    modulo = 'Afiliaciones'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = AfiliacionModel.objects.all()
    # mapping serializer into the action, this permit select different serializers, accordin to the action
    serializer_classes = {
        'update': ActualizarAfiliacionSerializer,
        'retrieve': DetalleAfiliacionSerializer
        # ... other actions
    }
    default_serializer_class = AfiliacionSerializer #  Default serializer

    # Override your get_serializer_class method.
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request, pk): # pk = id del afiliado
        
        query = AfiliacionModel.objects.filter(afiliado_id = pk).values(
            'id','afiliado_id','regimen','regimen__description','fecha_afiliacion','fecha_vencimiento','status_afiliacion',
            'aseguradora_id','aseguradora_id','aseguradora_id__description','ips_primaria','ips_primaria__ips',
            'created','owner','active'
        )
        serializer = AfiliacionSerializer(data=list(query), many=True)
        if serializer.is_valid():
            return Response(list(query), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):

        # Peticion POST para crear una cohorte a un afiliado
        serializer = AfiliacionSerializer(data=request.data)
        try:
            request.data['owner'] = request.user.id          
        except:
            pass
        # TODO reglas de validacion para que no se solapen fechas de afiliacion, preguntar
        if serializer.is_valid():    
            # Antes de crear el registro, cambia los demas registros de afiliacion a False, si existen
            AfiliacionModel.objects.filter(afiliado_id = request.data['afiliado_id']).update(status_afiliacion=False)
            # Check dates to validated if date afiliacion less than date vencimiento
            _rule1 = AfiliacionMayorVencimientoRule(
                request.data['fecha_afiliacion'], 
                request.data['fecha_vencimiento']).validate()
            if _rule1[0]:
                return Response(_rule1[1], status=status.HTTP_409_CONFLICT)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None): 
        # Petiion GET para retornar las cohortes asignadas a un afiliado
        query = AfiliacionModel.objects.filter(id = pk).all()
        serializer = DetalleAfiliacionSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None): # pk = id de la afiliacion
        # se obtiene el id de afiliado
        query_afiliacion = AfiliacionModel.objects.filter(id=pk).all().last()
        serializer_afiliacion = AfiliacionSerializer(query_afiliacion)
        afiliado_id = serializer_afiliacion.data['afiliado_id']
        
        data_update = request.data   
        serializer = ActualizarAfiliacionSerializer(data=data_update)
        # TODO reglas de validacion para que no se solapen fechas de afiliacion, preguntar
        if serializer.is_valid():
            # Si el registro a actualizar activa el estatus de afiliacion, los demas se desactivan
            if 'status_afiliacion' in data_update.keys():
                if data_update['status_afiliacion']:
                    AfiliacionModel.objects.filter(afiliado_id = afiliado_id).update(status_afiliacion=False)
            # Se actualiza el registro de afiliacion
            AfiliacionModel.objects.filter(id=pk).update(**data_update)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)       
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

    def destroy(self, request, pk=None):
        '''
        Borra un registro de afiliacion
        '''

        # TODO impletar logs
        AfiliacionModel.objects.filter(id = pk ).delete()
        return Response(status=status.HTTP_202_ACCEPTED)
