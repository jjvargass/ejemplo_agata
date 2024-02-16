# -*- coding: utf-8 -*-
# from odoo import http


# class EjemploAgata(http.Controller):
#     @http.route('/ejemplo_agata/ejemplo_agata', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ejemplo_agata/ejemplo_agata/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ejemplo_agata.listing', {
#             'root': '/ejemplo_agata/ejemplo_agata',
#             'objects': http.request.env['ejemplo_agata.ejemplo_agata'].search([]),
#         })

#     @http.route('/ejemplo_agata/ejemplo_agata/objects/<model("ejemplo_agata.ejemplo_agata"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ejemplo_agata.object', {
#             'object': obj
#         })
