from django.urls import path as path_django
from objeciones.views.objeciones import ObjecionesView
from objeciones.views.tipos_objeciones import TipoObjecionesView
from pyrsistent import s
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings




schema_view = get_swagger_view(title='APP Objeciones SIRIUS')


router = DefaultRouter()

urlpatterns = [
    path_django('tipo-objeciones', TipoObjecionesView.as_view({
        'get':'list',
        'post':'create'
    })),
    path_django('objecion', ObjecionesView.as_view({
        'get':'list',
        'post':'create'
    })),
    path_django('objecion/<str:pk>', ObjecionesView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    }))

]

urlpatterns += router.urls