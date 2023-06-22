# -*- coding: utf-8 -*-
# from odoo import http


# class Retribusi(http.Controller):
#     @http.route('/retribusi/retribusi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/retribusi/retribusi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('retribusi.listing', {
#             'root': '/retribusi/retribusi',
#             'objects': http.request.env['retribusi.retribusi'].search([]),
#         })

#     @http.route('/retribusi/retribusi/objects/<model("retribusi.retribusi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('retribusi.object', {
#             'object': obj
#         })
