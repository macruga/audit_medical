# from django.shortcuts import render
from core.paginations import CustomPaginationAfiliados
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from eventos.models.eventos_estancias import EventosEstanciaModel
from eventos.serializers.eventos_estancias import EventosEstanciaSerializer
from eventos.validators import EventosValidator

# Permissions
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered   # Path to our custom permission

class EventosEstanciasView(viewsets.ModelViewSet):
  # All views must contain a model  name for the permissions are efective:
  modulo = 'eventos'
  # Call classes for authorization model 
  queryset = EventosEstanciaModel.objects.all()
  permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)  
  serializer_class = EventosEstanciaSerializer
  pagination_class = CustomPaginationAfiliados

  def list(self, request):
    '''
     Get all eventos adversos from estancia
    '''
    try:
      estancia = request.GET.get('estancia', '')
      if estancia != '':
        queryset = EventosEstanciaModel.objects.filter(estancia_id=estancia, estancia_id__estado = True)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = EventosEstanciaSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = EventosEstanciaSerializer(queryset, many=True)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
      else:
        return Response("Debe indicar el parametro estancia", status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

  def create(self, request, *args, **kwargs):
    #validation
    try:
        serializer = EventosEstanciaSerializer(data=request.data)
        # Assign owner from loggin user, if API fill it, get inmutable error, then pass
        try:
            request.data['owner'] = request.user.id            
        except:
            pass

        if serializer.is_valid():       
            validate = EventosValidator(data=request.data, serializer=serializer)   
            return validate.creacionEvento()               
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
          return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
  
  def retrieve(self, request, pk=None):
    #Validation
    try:
      query = EventosEstanciaModel.objects.get(id=pk)
      serializer = EventosEstanciaSerializer(query)
      return Response(serializer.data)
    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    try:
      serializer = EventosEstanciaSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      validator = EventosEstanciaModel
      return validator.medicamentoUpdateValidator(pk=pk, data=request.data)

    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
    EventosEstanciaModel.objects.filter(id = pk ).delete()
    return Response(status=status.HTTP_200_OK)

