# -*- coding: utf-8 -*-
from odoo import http

# class FieldsFunctionsJarochito(http.Controller):
#     @http.route('/fields_functions_jarochito/fields_functions_jarochito/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fields_functions_jarochito/fields_functions_jarochito/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fields_functions_jarochito.listing', {
#             'root': '/fields_functions_jarochito/fields_functions_jarochito',
#             'objects': http.request.env['fields_functions_jarochito.fields_functions_jarochito'].search([]),
#         })

#     @http.route('/fields_functions_jarochito/fields_functions_jarochito/objects/<model("fields_functions_jarochito.fields_functions_jarochito"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fields_functions_jarochito.object', {
#             'object': obj
#         })