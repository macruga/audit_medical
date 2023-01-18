"""
Clase para la logica de la creacion del paciente

En la creación de un nuevo paciente Validar si ya existe un paciente con los datos suministrados, de ser así, no se ejecutara 
la creación y en cambio se deberán validar las siguientes posibilidades:
Paciente en estado egresado, se creara una estancia nueva y en el mensaje de respuesta se debe indicar que el paciente ya existía y se ha creado una nueva estancia.
Paciente en estado ingresado, el paciente ya esta creado y con estancia activa, no se debe realizar ninguna acción y se emitirá una mensaje informando del evento.
Paciente en estado fallecido, no se realiza acción, se emite mensaje informando que el paciente se encuentra en estado fallecido.

"""

import string
from typing import Dict
from afiliados.models.afiliado import afiliadoModel


class EstPacienteNuevo:

    def __init__(self, NumIdentificacion: string) -> None:

        self.NumIdentificacion = NumIdentificacion
        self.resp = {
            'status': False,
            'msg': '',
            'estancia': 0
        }

        


    def validate(self) -> Dict:
        afiliado_existe = afiliadoModel.objects.filter(identificacion = self.NumIdentificacion).exists()

        if afiliado_existe:
            afiliado_egresado = afiliadoModel.objects.filter(
                identificacion = self.NumIdentificacion, estado_paciente = 'E').exists()

            if afiliado_egresado:
                # TODO Crear una nueva estancia
                self.resp['status'] = True
                self.resp['msg'] = 'El afiliado existe en estado egresado, se ha creado una nueva estancia'
                self.resp['estancia'] = 1000 # TODO debe retornar el id de la estancia creada

                # Cambia el estado del paciente
                afiliadoModel.objects.filter(identificacion = self.NumIdentificacion).update(
                    estado_paciente = 'I'
                )
                return self.resp

    
            afiliado_fallecido = afiliadoModel.objects.filter(
                identificacion = self.NumIdentificacion, estado_paciente = 'F').exists()

            if afiliado_fallecido:
                self.resp['status'] = True
                self.resp['msg'] = 'El afiliado existe en estado fallecido, no se ha realizado ninguna accion'
                return self.resp

            afiliado_ingresado = afiliadoModel.objects.filter(
                identificacion = self.NumIdentificacion, estado_paciente = 'I').exists()

            if afiliado_ingresado:
                # TODO Generar consulta para obtener el ID de la estancia activa del paciente
                self.resp['status'] = True
                self.resp['msg']  = 'El afiliado existe en estado ingresado, tiene una estancia activa'
                self.resp['estancia'] = 1000 # TODO debe retornar el id de la estancia activa
                return self.resp

        else:
            return self.resp

