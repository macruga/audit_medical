#permissions.py
from rest_framework.permissions import BasePermission
from core.models.grupo_perfil import GrupoPerfil
from core.models.perfiles import PerfilModel
from core.models.modulos_app import ModuloApp
from django.contrib.auth.models import ContentType
from core.models.usuarios import UserModel

# ip_addr = request.META['REMOTE_ADDR']
# domain = request.META['REMOTE_HOST']


# Custom permission for users with "is_active" = True.
class IsActive(BasePermission):
       message = "El usuario no se encuentra activo"
       def has_permission(self, request, view):
              validation = request.user and request.user.is_active
              return validation

# Validate if model is registered into permissions
class IsModelRegistered(BasePermission):
       message = "El modulo no se encuentra registrado, ver documentacion"
       def has_permission(self, request, view):
              # Si es un super usuario tiene acceso a todos los modulos
              if request.user and request.user.is_superuser:
                     return True
              try:
                     return ModuloApp.objects.filter( modulo = str(view) ).exists()
              except:
                     return False

class IsProfileAuth(BasePermission):
       message = "El perfil o grupo del usuario no permite esta accion, valide que el usuario tenga un grupo asignado y los permisos correspondientes"
       def has_permission(self, request, view):

              '''Super User has all permissions'''
              if request.user and request.user.is_superuser:
                     return True
              
              '''Check if user has a group assigned'''
              groupCheck = UserModel.objects.filter(username=request.user).values('group_profile')
              # print(groupCheck)

              if not groupCheck:
                     return False

              ''' if user has a group assigned, check if group has permissions'''       
              validation = False
              for group in groupCheck:
                     # groupCheck = GroupProfile.objects.filter(id = request.user.group_profile).exists()
                     # If user has grupo, check permissions for model and request
                     # model_id = ContentType.objects.filter( model = str(view) )
                     profileCheck = PerfilModel.objects.filter( group = group['group_profile'], modulo__modulo = view )
                     if profileCheck.count():
                            for profile in profileCheck:
                                   if request.method == 'GET':
                                          validation = validation or profile.read
                                   if request.method == 'POST':
                                          validation = validation or profile.write
                                   if request.method == 'PUT':
                                          validation =  validation or profile.update
                                   if request.method == 'OPTIONS':
                                          validation = validation or profile.options
                                   if request.method == 'DELETE':
                                          validation = validation or profile.delete
                                   if request.method == 'PATCH':
                                          validation = validation or profile.patch
              return validation
           