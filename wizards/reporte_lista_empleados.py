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
    archivo = fields.Binary('Archivo',readonly=True,filters="xls")
    nombre_archivo = fields.Char('Nombre del Archivo', size=255)

    def action_reporte_lista_empleados(self):
        print("hola")