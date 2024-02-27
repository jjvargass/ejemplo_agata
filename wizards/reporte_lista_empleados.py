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
        print("hola")