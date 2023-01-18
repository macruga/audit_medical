# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation
# importar los elementos de las otras bases de datos
from afiliados.models.afiliado import afiliadoModel
from afiliados.models.afiliacion import afiliacionModel

# Modelo de los tipos de hospitalizacion
class pacienteModel(models.Model):
    '''
    Modelo de la relación (objeto) paciente (temporal)

    Attributes
    ----------
    id: long
        Identificador del paciente
    afiliado_id: int
        Código del paciente afiliado
    afiliacion_id: int
        Código identificador de la afiliación del paciente
    '''
    afiliado_id = models.ForeignKey(
        afiliadoModel, 
        help_text="Identificador del afiliado", 
        related_name="paciente_afiliado_atencion", 
        on_delete=models.PROTECT, 
        db_column="afiliado_id"
        )
        
    afiliacion_id = models.ForeignKey(
        afiliacionModel, 
        help_text="Identificador de la afiliacion", 
        related_name="paciente_afiliacion_atencion", 
        on_delete=models.PROTECT, 
        db_column="afiliacion_id"
        )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_paciente', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description  )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'