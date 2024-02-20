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
        #required=True,
        track_visibility='onchange',
        comodel_name='hr.employee',
        ondelete='restrict',
        help='''Empleado para Reporte''',
        domain= "[('user_id','!=',False)]",
    )
    archivo = fields.Binary('Archivo',readonly=True,filters="xls")
    nombre_archivo = fields.Char('Nombre del Archivo', size=255)

    def action_crear_reporte(self):
        all_data = {
            "nombre_empleado": 'JOSE JAVIER VARGAS SERRATO',
            "beingPaidForIt": False,
        }

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
