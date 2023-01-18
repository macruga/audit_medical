# from django.shortcuts import render
import datetime
from core.paginations import CustomPaginationAfiliados
from objeciones.models.objeciones import ObjecionModel
from objeciones.serializers.objeciones import ObjecionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from core.models.soporte.cums import CumsModel
from estancias.models.estancia import EstanciaModel
from medicamentos.models import MedicamentoModel
from medicamentos.serializers import AsesorSerializer, AsesoriaSerializer, MedicamentoSerializer, PertinenciaSerializer
from medicamentos.validators import MedicamentoValidator
# Permissions
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered   # Path to our custom permission

class MedicamentoView(viewsets.ModelViewSet):
  # All views must contain a model  name for the permissions are efective:
  modulo = 'medicamentos'
  # Call classes for authorization model 
  queryset = MedicamentoModel.objects.all()
  permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)  
  serializer_class = MedicamentoSerializer
  pagination_class = CustomPaginationAfiliados

  def list(self, request):
    '''
     Get all medicamentos from estancia
    '''
    try:
      estancia = request.GET.get('estancia', '')
      if estancia != '':
        queryset = MedicamentoModel.objects.filter(estancia_id=estancia, estancia_id__estado = True)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = MedicamentoSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = MedicamentoSerializer(queryset, many=True)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
      else:
        return Response("Debe indicar el parametro estancia", status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

  def create(self, request, *args, **kwargs):
    #validation
    try:
        serializer = MedicamentoSerializer(data=request.data)
        # Assign owner from loggin user, if API fill it, get inmutable error, then pass
        try:
            request.data['owner'] = request.user.id            
        except:
            pass

        if serializer.is_valid():       
            validate = MedicamentoValidator(data=request.data, serializer=serializer)   
            return validate.estanciaMedicamentos()               
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
          return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
  
  def retrieve(self, request, pk=None):
    #Validation
    try:
      query = MedicamentoModel.objects.get(id=pk)
      serializer = MedicamentoSerializer(query)
      return Response(serializer.data)
    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    try:
      serializer = MedicamentoSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      validator = MedicamentoValidator
      return validator.medicamentoUpdateValidator(pk=pk, data=request.data)

    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
    return Response(status=status.HTTP_401_UNAUTHORIZED)


class MedicamentosEstanciasView(viewsets.ModelViewSet):
  # All views must contain a model  name for the permissions are efective:
  modulo = 'medicamentos'
  # Call classes for authorization model 
  permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)  
  serializer_class = MedicamentoSerializer
  pagination_class = CustomPaginationAfiliados
  '''
     Get all medicamentos from estancias active 
  '''
  def list(self, request):
    try:
      queryset = MedicamentoModel.objects.filter(estancia_id__estado = True) 
      page = self.paginate_queryset(queryset)
      if page is not None:
          serializer = MedicamentoSerializer(page, many=True)
          result = self.get_paginated_response(serializer.data)
          data = result.data # pagination data
      else:
          serializer = self.MedicamentoSerializer(queryset, many=True)
          data = serializer.data
      serializer = MedicamentoSerializer(queryset, many=True)
      return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MedicamentosHistView(viewsets.ModelViewSet):
  # All views must contain a model  name for the permissions are efective:
  modulo = 'medicamentos'
  # Call classes for authorization model 
  permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)  
  serializer_class = MedicamentoSerializer
  pagination_class = CustomPaginationAfiliados
  '''
     Get all medicamentos from estancias active 
  '''
  def list(self, request):
    try:
      queryset = MedicamentoModel.objects.all()
      page = self.paginate_queryset(queryset)
      if page is not None:
          serializer = MedicamentoSerializer(page, many=True)
          result = self.get_paginated_response(serializer.data)
          data = result.data # pagination data
      else:
          serializer = self.MedicamentoSerializer(queryset, many=True)
          data = serializer.data
      serializer = MedicamentoSerializer(queryset, many=True)
      return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MedicamentoPertinenciaView(viewsets.ModelViewSet):
  # All views must contain a model  name for the permissions are efective:
  modulo = 'medicamento-pertinencia'
  # Call classes for authorization model 
  permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)  
  serializer_class = PertinenciaSerializer
  '''
     Update pertinencia medicamento 
  '''
  def update(self, request, pk=None):
    try:
        request.data['auditor'] = request.user.id            
    except:
        pass
    try:
      serializer = PertinenciaSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      validator = MedicamentoValidator(data=request.data, serializer=serializer)
      return validator.pertinenciaMedicamentos(pk=pk)

    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MedicamentoAsesoriaView(viewsets.ModelViewSet):
  # All views must contain a model  name for the permissions are efective:
  modulo = 'medicamento-asesoria'
  # Call classes for authorization model 
  permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)  
  serializer_class = AsesoriaSerializer
  '''
     Update solicitud asesoria medicamento 
  '''
  def update(self, request, pk=None):
    try:
        request.data['usuario_solicitud'] = request.user.id            
    except:
        pass
    try:
      serializer = AsesoriaSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      validator = MedicamentoValidator(data=request.data, serializer=serializer)
      return validator.asesoriaMedicamentos(pk=pk)

    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MedicamentoAsesorView(viewsets.ModelViewSet):
  # All views must contain a model  name for the permissions are efective:
  modulo = 'medicamento-asesor'
  # Call classes for authorization model 
  permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)  
  serializer_class = AsesorSerializer
  '''
     Update detalle asesor medicamento 
  '''
  def update(self, request, pk=None):
    try:
        request.data['asesor'] = request.user.id            
    except:
        pass
    try:
      serializer = AsesorSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      validator = MedicamentoValidator(data=request.data, serializer=serializer)
      return validator.asesorMedicamentos(pk=pk)

    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MedicamentoObjecionView(viewsets.ModelViewSet):
  # All views must contain a model  name for the permissions are efective:
  modulo = 'medicamento-objecion'
  # Call classes for authorization model 
  
  permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)  
  queryset = ObjecionModel.objects.all()
  serializer_class = ObjecionSerializer
  '''
     Crate objetion medicamento 
  '''

  def create(self, request, *args, **kwargs):
    #validation
    try:
      serializer = ObjecionSerializer(data=request.data)
      # Assign owner from loggin user, if API fill it, get inmutable error, then pass
      try:
          request.data['owner'] = request.user.id            
      except:
          pass

      if serializer.is_valid():       
          validate = MedicamentoValidator(data=request.data, serializer=serializer)   
          return validate.objecionMedicamentos()               
      else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
          return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

