# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    is_lot_id_editable = fields.Boolean(
        string="Is lot editable?",
        compute="_compute_is_lot_id_editable",
        help="Technical field to define if the 'lot_id' field is editable.",
    )

    @api.depends("lot_id")
    def _compute_is_lot_id_editable(self):
        for line in self:
            line.is_lot_id_editable = True
            mos = line.move_id.move_orig_ids.production_id
            lot_prapagated = [
                mo.propagated_lot_producing == line.lot_id.name
                and mo.subcontracting_has_been_recorded
                and mo.is_lot_number_propagated
                for mo in mos
            ]
            if any(lot_prapagated):
                line.is_lot_id_editable = False

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        # Override to make readonly the "lot_id" field if 'is_lot_editable' is false.
        # This is done this way as it's not possible to update easily existing 'attrs'
        # attributes on all views.
        arch, view = super()._get_view(view_id, view_type, **options)
        if arch.xpath("//field[@name='is_lot_id_editable']"):
            arch = self._fields_view_get_adapt_lot_tags_attrs(arch)
        return arch, view

    def _fields_view_get_adapt_lot_tags_attrs(self, arch):
        """Set as readonly 'lot_id' field if 'is_lot_editable' is false."""
        tags = ("//field[@name='quant_id']","//field[@name='lot_id']","//field[@name='lot_name']")
        for xpath_expr in tags:
            nodes = arch.xpath(xpath_expr)
            for field in nodes:
                attr_invisible = field.attrib.get("readonly", "")
                if not attr_invisible:
                    field.attrib["readonly"] = "not is_lot_id_editable"
                else:
                    field.attrib["readonly"] = (
                        field.attrib["readonly"] + " or not is_lot_id_editable"
                    )
        return arch
