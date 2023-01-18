"""
Para generar las migraciones iniciales generar makemigrations por 
cada uno de los imports
 
"""
 
from core.models.usuarios import UserModel
from core.models.grupo_perfil import GrupoPerfil
 
from core.models.modulos_app import ModuloApp
from core.models.perfiles import PerfilModel
from core.models.soporte.cie10 import Cie10Model
from core.models.soporte.tipo_documento import TipoDocumentoModel
from core.models.soporte.cums import CumsModel
from core.models.soporte.sexo import SexoModel
from core.models.soporte.departamentos import DepartamentoModel
from core.models.soporte.municipios import MunicipioModel
from core.models.soporte.zona_residencia import ZonaResidenciaModel
from core.models.soporte.codigos_consulta import CodigosConsultaModel
from core.models.soporte.cif import CifModel
from core.models.soporte.cohorte import CohorteModel
from core.models.soporte.escolaridad import EscolaridadModel
from core.models.soporte.estado_civil import EstadoCivilModel
from core.models.soporte.grupo_poblacional import GrupoPoblacionalModel
from core.models.soporte.ocupacion import OcupacionModel
from core.models.soporte.origen_etnico import OrigenEtnicoModel
from core.models.soporte.vulnerabilidad import VulnerabilidadModel
from core.models.soporte.ips import IpsModel
from core.models.soporte.paises import PaisModel
from core.models.soporte.atc import AtcModel
from core.models.soporte.cups import CupsModel
from core.models.soporte.servicios import ServiciosModel
from core.models.soporte.especialidades import EspecialidadesModel


