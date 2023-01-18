from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view




schema_view = get_swagger_view(title='Modulo afiliados core SIRIUS')

from afiliados.views.afiliacion import AfiliacionView
from afiliados.views.afiliado_cohorte import CohorteAfiliadoView
from core.views.soporte.cohorte import CohorteView
from afiliados.views.afiliado import AfiliadoView, AfiliadosIngresadosView, AfiliadoSearchView

router = DefaultRouter()


urlpatterns = [
    path('afiliados', AfiliadoView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('afiliado/<str:pk>', AfiliadoView.as_view({
        'get':'retrieve',
        'put':'update'
    })),
    path('afiliados-ingresados', AfiliadosIngresadosView.as_view({
        'get':'list'
    })),
    path('cohorte', CohorteView.as_view({
        'post':'create',
        'get':'list'
    })),
    path('cohorte/<str:pk>', CohorteView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('cohortes', CohorteAfiliadoView.as_view({
        'post':'create'
    })),
    path('cohortes-afiliado/<str:pk>', CohorteAfiliadoView.as_view({
        'get':'list'
    })),
    path('cohorte-afiliado/<str:pk>', CohorteAfiliadoView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('afiliaciones', AfiliacionView.as_view({
        'post':'create'
    })),
    path('afiliaciones-afiliado/<str:pk>', AfiliacionView.as_view({
        'get':'list'
    })),
    path('afiliacion/<str:pk>', AfiliacionView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('search', AfiliadoSearchView.as_view({
        'get':'list'
    })),
    path('swagger-docs/', schema_view)
]

urlpatterns += router.urls
