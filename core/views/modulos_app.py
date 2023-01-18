from rest_framework import viewsets

# Imports propios
from core.models.modulos_app import ModuloApp
from core.serializers.modulos_app import ModuloAppSerializer
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 

class ModuloAppView(viewsets.ModelViewSet):
    # All views must contein a model  name for the permissions are efective, we get this from serializer, see:
    modulo = 'ModuloApp'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth,)
    queryset = ModuloApp.objects.all()
    serializer_class = ModuloAppSerializer
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )