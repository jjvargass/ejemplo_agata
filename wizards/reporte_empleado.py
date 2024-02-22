from odoo import models, fields, api
from odoo.addons.base_agata.tools import build_office_reports
from odoo.exceptions import ValidationError
import os


class BaseAgataWizardTest(models.TransientModel):
    _name = 'ejemplo_agata.wizard.test'
    _description = 'Test Wizard 01'

    # -------------------
    # Fields
    # -------------------

    empleado = fields.Many2one(
        string='Empleado',
        track_visibility='onchange',
        comodel_name='hr.employee',
        ondelete='restrict',
        help='''Empleado para Reporte''',
    )
    archivo = fields.Binary('Archivo',readonly=True,filters="xls")
    nombre_archivo = fields.Char('Nombre del Archivo', size=255)


    def action_crear_reporte(self):
        # Construir data
        all_data = self.get_informacion_contrato()

        # Ruta Actual
        separador = os.path.sep  # obtiene segun el sistema operativo
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        dir_modulo = separador.join(dir_actual.split(separador)[:-1])

        # Directorio reportes
        dir_report = os.path.join(dir_modulo, 'office_reports')

        if not os.path.exists(dir_report):
            raise ValidationError("Debe establecer directorio de reportes [office_reports] para este módulo")

        documento = build_office_reports.create_office_reports(
            self,
            all_data,
            "REPORTE_AGATA",
            "pdf",
            "reporte_empleados.odt",
            dir_report
        )
        self.archivo = documento[0]
        self.nombre_archivo = documento[1]

        # busamos el wizar de descarga
        view_ids = self.env['ir.ui.view'].search([
            ('model','=','ejemplo_agata.wizard.test'),
            ('name','=','ejemplo_agata.crear_reporte.view_form_download')
        ])

        # Retornar Vista
        return {
                'view_type':'form',
                'view_mode':'form',
                'res_model':'ejemplo_agata.wizard.test',
                'target':'new',
                'type':'ir.actions.act_window',
                'view_id':view_ids.id,
                'res_id': self.id,
        }


    def get_informacion_contrato(self):
        contrato = self.env['hr.contract'].search([
            ('employee_id', '=', self.empleado.id),
            ('state', '=', 'open' ),
        ])
        nomb_empleado = self.empleado.name.upper()

        if (len(contrato) == 0):
            raise ValidationError("El Empleado " + nomb_empleado + " no tiene Contratos Activos")
        elif (len(contrato) > 1):
            raise ValidationError("El Empleado " + nomb_empleado + " tiene mas de 1 contrato activo. \nSe de actualizar los estado de los contatos.\nRecuerde que no esta permitido tener mas de 1 contrato activo.")

        data_contrato = {
            "nombre_empleado": nomb_empleado,
            "num_cedula" : self.empleado.identification_id,
            "fecha_inicio_contrato" : contrato.date_start,
            "cargo_empleado" : self.empleado.job_id.name,
            "tipo_contrato_empleado" : contrato.contract_type_id.name,
        }
        return data_contrato
