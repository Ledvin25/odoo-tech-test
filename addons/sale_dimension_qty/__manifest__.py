# -*- coding: utf-8 -*-
{
    "name": "Sale Dimension Quantity",
    "summary": "Deriva la cantidad de venta desde Largo × Ancho × Alto",
    "version": "18.0.1.0.0",
    "author": "Ledvin Leiva",
    "license": "LGPL-3",
    "depends": ["sale", "sale_management"],
    "data": [
        "views/sale_order_views.xml", "report/sale_report.xml"
    ],
    "installable": True,
    "application": False,
}
