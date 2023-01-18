from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_swagger_view(title='API Censo SIRIUS')

from censo.views.censo_uploads import uploadFileCensoView, uploadsUserView


router = DefaultRouter()

router.register('upload-censo', uploadFileCensoView, basename='Censo upload file')
router.register('uploads-user', uploadsUserView, basename='Uploads Users')

urlpatterns = []

urlpatterns += router.urls