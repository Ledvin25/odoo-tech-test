# sale_dimension_qty/tests/test_sale_dimension_qty.py
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
from odoo.tools import float_compare

@tagged('sale_dimension_qty', 'post_install', '-at_install')
class TestSaleDimensionQty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")

        cls.product_consu = cls.env["product.product"].create({
            "name": "Panel 3D",
            "lst_price": 100.0,
            "type": "consu",
            "uom_id": cls.uom_unit.id,
            "uom_po_id": cls.uom_unit.id,
        })
        cls.product_service = cls.env["product.product"].create({
            "name": "Servicio 3D",
            "lst_price": 50.0,
            "type": "service",
            "uom_id": cls.uom_unit.id,
            "uom_po_id": cls.uom_unit.id,
        })

        cls.so = cls.env["sale.order"].create({
            "partner_id": cls.partner.id,
        })

    def _fc(self, a, b, digits=2):
        return float_compare(a, b, precision_digits=digits)

    def test_01_qty_and_subtotal_consu(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.so.id,
            "product_id": self.product_consu.id,
            "product_uom": self.uom_unit.id,
            "x_length": 2.0,
            "x_width": 3.0,
            "x_height": 4.0,
        })
        self.assertEqual(line.product_uom_qty, 24.0)
        self.assertEqual(self._fc(line.price_subtotal, 2400.0), 0)

        line.write({"x_height": 1.0})
        self.assertEqual(line.product_uom_qty, 6.0)
        self.assertEqual(self._fc(line.price_subtotal, 600.0), 0)

    def test_02_qty_and_subtotal_service(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.so.id,
            "product_id": self.product_service.id,
            "product_uom": self.uom_unit.id,
            "x_length": 1.5,
            "x_width": 2.0,
            "x_height": 2.0,
        })
        self.assertEqual(self._fc(line.product_uom_qty, 6.0), 0)
        self.assertEqual(self._fc(line.price_subtotal, 300.0), 0)

    def test_03_validation_non_negative(self):
        line = self.env["sale.order.line"].create({
            "order_id": self.so.id,
            "product_id": self.product_consu.id,
            "product_uom": self.uom_unit.id,
            "x_length": 1.0, "x_width": 1.0, "x_height": 1.0,
        })
        with self.assertRaises(ValidationError):
            line.write({"x_width": -0.5})
