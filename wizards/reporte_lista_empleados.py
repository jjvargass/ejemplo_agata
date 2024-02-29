from odoo import models, fields, api
from odoo.addons.base_agata.tools import build_office_reports
from odoo.exceptions import ValidationError
import os

class BaseAgataWizardListaEmpleado(models.TransientModel):
    _name = 'ejemplo_agata.wizard.lista.empleados'
    _description = 'Test Wizard Lista de empleados xls por dependencias'

    # -------------------
    # Fields
    # -------------------

    departamento = fields.Many2one(
        string='Departamento',
        comodel_name='hr.department',
        ondelete='restrict',
        help='''Departamento''',
    )
    archivo = fields.Binary(
        string='Archivo',
        readonly=True,
        help='''Archivo binario para descargas''',
    )
    nombre_archivo = fields.Char(
        string='Nombre del Archivo',
        size=255,
        help='''String para nombre del archivo a descargar''',
    )

    def action_reporte_lista_empleados(self):
        # Construir data
        all_data = self.get_informacion_empleado()

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
            "REPORTE_LISTA_EMPLEADOS_AGATA",
            "xls",
            "repote_por_dependencia.ods",
            dir_report
        )
        self.archivo = documento[0]
        self.nombre_archivo = documento[1]

        # busamos el wizar de descarga
        view_ids = self.env['ir.ui.view'].search([
            ('model','=','ejemplo_agata.wizard.lista.empleados'),
            ('name','=','ejemplo_agata.reporte_lista_empleados.view_form_download')
        ])

        # Retornar Vista
        return {
            'view_type':'form',
            'view_mode':'form',
            'res_model':'ejemplo_agata.wizard.lista.empleados',
            'target':'new',
            'type':'ir.actions.act_window',
            'view_id':view_ids.id,
            'res_id': self.id,
        }

    def get_informacion_empleado(self):
        if not self.departamento:
            empleados = self.env['hr.employee'].search([])
            if (len(empleados) == 0):
                raise ValidationError("No Existen Empleado.")
        else:
            empleados = self.env['hr.employee'].search([
                ('department_id', '=', self.departamento.id),
            ])
            if (len(empleados) == 0):
                raise ValidationError("No Existen Empleado asociados al departamento " + self.departamento.name + ".")

        all_empelados = []
        for empleado in empleados:
            data_empelado = {
                "nombre": empleado.name,
                "email" : empleado.work_email,
                "cel" : empleado.work_phone,
                "departamento" : empleado.department_id.name,
            }
            all_empelados.append(data_empelado)

        all_data = {
            "empleados" : all_empelados
        }
        return all_data
