# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def subcontracting_record_component(self):
        if self.is_lot_number_propagated and self.propagated_lot_producing:
            self._create_and_assign_propagated_lot_number()
        res = super().subcontracting_record_component()

        # Workaround:
        if 'res_id' in res:
            res_id = res['res_id']
            backorder = self.browse(res_id)
            resupply = backorder.picking_ids
            used_lot_ids = []
            for production in self.procurement_group_id.mrp_production_ids:
                used_lot_ids.extend(production.move_line_raw_ids.lot_id.mapped('id'))
            for move_line in backorder.move_line_raw_ids:
                if move_line.lot_id:
                    continue
                for supply_move_line in resupply.move_line_ids:
                    lot_id = supply_move_line.lot_id.id
                    if supply_move_line.product_id.id != move_line.product_id.id or lot_id in used_lot_ids:
                        continue

                    move_line.lot_id = lot_id
                    used_lot_ids.append(lot_id)
                    break
        return res

    def _views_to_adapt(self):
        names = super()._views_to_adapt()
        return names + ["mrp.production.subcontracting.form.view"]

    @api.depends(
        # New field dependencies to compute the propagated lot on the
        # "mrp_production_subcontracting_form_view" view.
        "move_raw_ids.move_line_ids.quantity",
        "move_raw_ids.move_line_ids.lot_id",
        "move_line_raw_ids.lot_id",
    )
    def _compute_propagated_lot_producing(self):
        return super()._compute_propagated_lot_producing()

    # def _fields_view_get_adapt_lot_tags_attrs(self, arch):
    #     arch = super()._fields_view_get_adapt_lot_tags_attrs(arch)
    #     # Remove 'required' on 'lot_producing_id' if it is automatically propagated.
    #     tags = ("//field[@name='lot_producing_id']",)
    #     for xpath_expr in tags:
    #         nodes = arch.xpath(xpath_expr)
    #         for field in nodes:
    #             attr_invisible = field.attrib.get("required", "")
    #             if not attr_invisible:
    #                 field.attrib["required"] = "not is_lot_number_propagated"
    #             else:
    #                 field.attrib["required"] = (
    #                     field.attrib["required"] + " and not is_lot_number_propagated"
    #                 )
    #     return arch

    def _is_lot_producing_id_required_and_set(self):
        self.ensure_one()
        if not self.is_lot_number_propagated and not self.lot_producing_id and self.product_id.tracking in ("lot", "serial"):
            return True
        return False
