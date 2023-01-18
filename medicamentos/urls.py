from django.urls import path as path_django
from pyrsistent import s
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings

from medicamentos.views import MedicamentoAsesorView, MedicamentoAsesoriaView, MedicamentoObjecionView, MedicamentoPertinenciaView, MedicamentoView, MedicamentosEstanciasView


schema_view = get_swagger_view(title='APP Medicamentos SIRIUS')


router = DefaultRouter()

urlpatterns = [
   
    path_django('medicamentos', MedicamentoView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path_django('medicamento/<str:pk>', MedicamentoView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    })),path_django('medicamentos-estancias', MedicamentosEstanciasView.as_view({
        'get' : 'list'
    })),path_django('medicamento-pertinencia/<str:pk>', MedicamentoPertinenciaView.as_view({
        'put' : 'update',
    })),path_django('medicamento-asesoria/<str:pk>', MedicamentoAsesoriaView.as_view({
        'put' : 'update',
    })),path_django('medicamento-asesor/<str:pk>', MedicamentoAsesorView.as_view({
        'put' : 'update',
    })),path_django('medicamento-objecion', MedicamentoObjecionView.as_view({
        'post' : 'create',
    }))

    # 


    
]

urlpatterns += router.urls