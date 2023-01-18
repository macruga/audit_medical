from rest_framework import viewsets

# Imports propios
from core.models.perfiles import PerfilModel
from core.serializers.perfiles import PerfilSerializer
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 


class PerfilView(viewsets.ModelViewSet):
    # All views must contein a model  name for the permissions are efective, we get this from serializer, see:
    modulo = 'Perfil'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth,)
    queryset = PerfilModel.objects.all()
    serializer_class = PerfilSerializer
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )