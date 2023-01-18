from afiliados.models.afiliado import afiliadoModel
from estancias.models.estancia import EstanciaModel


class EgresoEstancia():

    '''         
        Clase para realizar egreso de una estancia

        Parameters
        ----------
         estancia_id: integer
            Id de la estancia a egresar

        fecha_ingreso: string
            Fecha de ingreso yyyy-mm-dd

        Returns
        -------
        validation: boolean
            True si se ha regisrado el egreso correctamente
        '''

    def __init__(self, estancia_id):
        self.estancia_id = estancia_id
        

    def Egresar(self):
        if not isinstance( self.estancia_id, int):
            self.estancia_id = int(self.estancia_id)
        EstanciaModel.objects.filter(id = self.estancia_id).update(estado = False)
        estancia = EstanciaModel.objects.filter(id = self.estancia_id).all().values()
        afiliadoModel.objects.filter(id = estancia[0]['afiliado_id_id']).update(estado_paciente_id = 'E')