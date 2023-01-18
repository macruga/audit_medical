from django.urls import path, include
from core.views.soporte.cums import CumsView
from core.views.soporte.tipos_asesores import TiposAsesoresView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings



schema_view = get_swagger_view(title='API Core SIRIUS')

from core.views.usuarios import LoginView, LogoutView, UserTokenView, \
                                UserJWTView, userView, passwordUpdate, UsersListView, UserPassword
from core.views.grupo_perfil import GroupPerfilView
from core.views.modulos_app import ModuloAppView
from core.views.perfiles import PerfilView
from core.views.soporte.cif import CifView
from core.views.soporte.departamentos import DepartamentoView
from core.views.soporte.escolaridad import EscolaridadView
from core.views.soporte.estado_civil import EstadoCivilView
from core.views.soporte.estados_paciente import EstadosPacienteView
from core.views.soporte.grupo_poblacional import GrupoPoblacionalView
from core.views.soporte.municipios import MunicipiosView
from core.views.soporte.ocupacion import OcupacionView
from core.views.soporte.origen_etnico import OrigenEtnicoView
from core.views.soporte.sexo import SexoView
from core.views.soporte.tipo_documento import TipoDocumentoView
from core.views.soporte.vulnerabilidad import VulnerabilidadView
from core.views.soporte.zona_residencia import ZonaResidenciaView
from core.views.soporte.aseguradoras import AseguradorasView
from core.views.soporte.ips import IpsView
from core.views.soporte.regimen import RegimenView
from censo.views.origen_evento import OrigenEventoView
from censo.views.tipo_ingreso import TipoIngresoView
from core.views.soporte.cie10 import Cie10View
from censo.views.tipo_habitacion import TipoHabitacionView
from core.views.soporte.especialidades import EspecialidadesView
from core.views.soporte.servicios import ServiciosView


router = DefaultRouter()

router.register('groups', GroupPerfilView, basename='group_profile')
router.register('profiles', PerfilView, basename='profiles')
router.register('modulos', ModuloAppView, basename='modulos_aplicacion')
router.register('usuarios', UsersListView, basename='usuarios')

urlpatterns = [
    path('users', UsersListView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('user/<str:pk>', UsersListView.as_view({
        'get':'retrieve',
        'put':'update'
    })),
    path('user_update/<str:pk>', UserPassword.as_view({
        'put':'update'
    })),
    path('user', userView.as_view(), name='user'),
    path('user_update', passwordUpdate.as_view({
        'put':'update'
    })),
    # path('password/', passwordUpdate.as_view(), name='password'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('user_token/', UserTokenView.as_view(), name = 'user_token'),
    path('user_jwt/', UserJWTView.as_view(), name = 'user_jwt'),
    path('api-auth', include('rest_framework.urls')),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtein'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger-docs/', schema_view),
    path('cif', CifView.as_view({
        'get':'list'
    })),
    path('departamentos', DepartamentoView.as_view({
        'get':'list'
    })),
    path('escolaridad', EscolaridadView.as_view({
        'get':'list'
    })),
    path('estado-civil', EstadoCivilView.as_view({
        'get':'list'
    })),
    path('estados-paciente', EstadosPacienteView.as_view({
        'get':'list'
    })),
    path('grupo-poblacional', GrupoPoblacionalView.as_view({
        'get':'list'
    })),
    path('ocupacion', OcupacionView.as_view({
        'get':'list'
    })),
    path('municipios', MunicipiosView.as_view({
        'get':'list'
    })),
    path('origen-etnico', OrigenEtnicoView.as_view({
        'get':'list'
    })),
    path('sexo', SexoView.as_view({
        'get':'list'
    })),
    path('tipo-documento', TipoDocumentoView.as_view({
        'get':'list'
    })),
    path('vulnerabilidad', VulnerabilidadView.as_view({
        'get':'list'
    })),
    path('zona-residencia', ZonaResidenciaView.as_view({
        'get':'list'
    })),
    path('aseguradoras', AseguradorasView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('aseguradoras/<str:pk>', AseguradorasView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('ips', IpsView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('ips/<str:pk>', IpsView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('regimen', RegimenView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('regimen/<str:pk>', RegimenView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('diagnostico', Cie10View.as_view({
        'get':'list',
        'post':'create'
    })),
    path('diagnostico/<str:pk>', Cie10View.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('tipo-ingreso', TipoIngresoView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('tipo-ingreso/<str:pk>', TipoIngresoView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('origen-evento', OrigenEventoView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('origen-evento/<str:pk>', OrigenEventoView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('tipo-habitacion', TipoHabitacionView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('tipo-habitacion/<str:pk>', TipoHabitacionView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('cums', CumsView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('cums/<str:pk>', CumsView.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('tipos-asesores', TiposAsesoresView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('tipos-asesores/<str:pk>', TiposAsesoresView.as_view({
        'get':'retrieve',
        'put':'update'
    })),
    path('especialidades', EspecialidadesView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path('especialidades/<str:pk>', EspecialidadesView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    })),
    path('servicios', ServiciosView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path('servicios/<str:pk>', ServiciosView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    }))
]

urlpatterns += router.urls
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)