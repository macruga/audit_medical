
from django.urls import path as path_django
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from eventos.views.eventos_adversos import EventosView
from eventos.views.eventos_estancias import EventosEstanciasView


schema_view = get_swagger_view(title = 'APP Eventos SIRIUS')


router = DefaultRouter()

urlpatterns = [
    path_django('eventos', EventosView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path_django('eventos/<str:pk>', EventosView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    })),
    path_django('eventos-estancias', EventosEstanciasView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path_django('eventos-estancias/<str:pk>', EventosEstanciasView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    }))
]

urlpatterns += router.urls