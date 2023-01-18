from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_swagger_view(title='API Medimas SIRIUS')

from medimas.views.carga_concurrencia import uploadFileConcurrenciaView


router = DefaultRouter()

router.register('carga-concurrencia', uploadFileConcurrenciaView, basename='Carga archivo de concurrencia')

urlpatterns = []

urlpatterns += router.urls