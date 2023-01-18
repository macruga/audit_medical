from django.urls import path as path_django
from pyrsistent import s
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_swagger_view(title='APP Estancias SIRIUS')

from estancias.views.estancia import EstanciaView, AnularEgresosView, EgresosView, IpsEstanciasActivas, WorklistView


router = DefaultRouter()

urlpatterns = [

    path_django('estancias', EstanciaView.as_view({
        'get':'list',
        'post':'create'
    })),
    path_django('estancias/<str:pk>', EstanciaView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path_django('anular-egreso/<str:pk>', AnularEgresosView.as_view({
        'put':'update',
    })),
    path_django('egreso/<str:pk>', EgresosView.as_view({
        'get':'retrieve',
        'put':'update',
    })),
    path_django('worklist', WorklistView.as_view({
        'get':'list',
        'post':'create'
    })),
    path_django('ips-estancias', IpsEstanciasActivas.as_view({
        'get':'list'
    }))
]

urlpatterns += router.urls