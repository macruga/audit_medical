
from django.urls import path as path_django
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from infecciones.views.germenes import GermenView
from infecciones.views.laboratoriosiaas import LabsIaasView
from infecciones.views.perfil_resistencia import PerfilResistenciaView
from infecciones.views.lugar_ocurrencia import LugarOcurrenciasView



schema_view = get_swagger_view(title = 'APP Infecciones SIRIUS')


router = DefaultRouter()

urlpatterns = [
    path_django('germen', GermenView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path_django('germen/<str:pk>', GermenView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    })),
    path_django('laboratorios', LabsIaasView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path_django('laboratorios/<str:pk>', LabsIaasView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    })),
        path_django('perfilresistencia', PerfilResistenciaView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path_django('perfilresistencia/<str:pk>', PerfilResistenciaView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    })),    
    path_django('lugarocurrencia', LugarOcurrenciasView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path_django('lugarocurrencia/<str:pk>', LugarOcurrenciasView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    }))
]

urlpatterns += router.urls