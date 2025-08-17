# -*- coding: utf-8 -*-
# from odoo import http


# class SaleDimensionQty(http.Controller):
#     @http.route('/sale_dimension_qty/sale_dimension_qty', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_dimension_qty/sale_dimension_qty/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_dimension_qty.listing', {
#             'root': '/sale_dimension_qty/sale_dimension_qty',
#             'objects': http.request.env['sale_dimension_qty.sale_dimension_qty'].search([]),
#         })

#     @http.route('/sale_dimension_qty/sale_dimension_qty/objects/<model("sale_dimension_qty.sale_dimension_qty"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_dimension_qty.object', {
#             'object': obj
#         })

