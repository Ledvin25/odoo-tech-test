# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Dimensiones (elige metros por defecto)
    x_length = fields.Float(
        string="Largo",
        default=0.0,
        help="Unidad: metros.",
    )
    x_width = fields.Float(
        string="Ancho",
        default=0.0,
        help="Unidad: metros.",
    )
    x_height = fields.Float(
        string="Alto",
        default=0.0,
        help="Unidad: metros.",
    )

    # Cantidad derivada (diagnóstico / auditoría)
    x_dimension_qty = fields.Float(
        string="Cantidad (L×A×H)",
        compute="_compute_dimension_qty",
        store=True,
        help="Cantidad derivada a partir de Largo × Ancho × Alto.",
    )

    # -------------------------
    # Cálculo base (compute)
    # -------------------------
    @api.depends("x_length", "x_width", "x_height")
    def _compute_dimension_qty(self):
        for line in self:
            l = max(line.x_length or 0.0, 0.0)
            w = max(line.x_width or 0.0, 0.0)
            h = max(line.x_height or 0.0, 0.0)
            line.x_dimension_qty = l * w * h

    # -------------------------
    # Aplicar qty derivada a product_uom_qty (con redondeo de la UoM)
    # -------------------------
    def _apply_dimension_qty_to_uom_qty(self):
        for line in self:
            # No tocar secciones / notas
            if line.display_type:
                continue
            qty = line.x_dimension_qty or 0.0
            rounding = (line.product_uom and line.product_uom.rounding) or 0.01
            line.product_uom_qty = float_round(qty, precision_rounding=rounding)

    # -------------------------
    # Onchange (UX) + warning si alguna dimensión es 0
    # -------------------------
    @api.onchange('x_length', 'x_width', 'x_height')
    def _onchange_dimensions(self):
        """Recalcula la cantidad y avisa si alguna dimensión es 0 (⇒ subtotal 0)."""
        for line in self:
            qty = (line.x_length or 0.0) * (line.x_width or 0.0) * (line.x_height or 0.0)
            line.product_uom_qty = qty

        # Mostrar un único warning cuando el onchange es sobre 1 línea
        if len(self) == 1:
            line = self
            if (not line.display_type and not line.is_downpayment
                    and any((v or 0.0) == 0.0 for v in (line.x_length, line.x_width, line.x_height))):
                return {
                    'warning': {
                        'title': _('Cantidad/Subtotal en 0'),
                        'message': _(
                            'Alguna dimensión es 0; la cantidad y el subtotal de la línea quedarán en 0.'
                        ),
                    }
                }

    # -------------------------
    # create / write (robustez para importaciones RPC)
    # -------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """(Tu create multi ya corregido) asegura product_uom_qty = L*W*H en creación."""
        for vals in vals_list:
            l = vals.get("x_length") or 0.0
            w = vals.get("x_width") or 0.0
            h = vals.get("x_height") or 0.0
            if "product_uom_qty" not in vals:
                vals["product_uom_qty"] = l * w * h

        lines = super().create(vals_list)
        for line in lines:
            qty = (line.x_length or 0.0) * (line.x_width or 0.0) * (line.x_height or 0.0)
            if line.product_uom_qty != qty:
                line.product_uom_qty = qty
        return lines

    def write(self, vals):
        res = super().write(vals)
        if {"x_length", "x_width", "x_height"} & set(vals.keys()):
            self._apply_dimension_qty_to_uom_qty()
        return res

    # -------------------------
    # Validación (no negativos)
    # -------------------------
    @api.constrains("x_length", "x_width", "x_height")
    def _check_non_negative(self):
        for line in self:
            for fname in ("x_length", "x_width", "x_height"):
                if getattr(line, fname) < 0:
                    raise ValidationError(_("Las dimensiones deben ser ≥ 0."))
