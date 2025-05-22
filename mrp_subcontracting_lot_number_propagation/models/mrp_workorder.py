# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from docutils.nodes import pending

from odoo import api, models, _
from odoo.exceptions import ValidationError

class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    def button_start(self, bypass=False):
        for wo in self:
            if wo.production_id.state in ('draft', 'confirmed') and wo.production_id._is_lot_producing_id_required_and_set():
                raise ValidationError(_("The Lot/Serial Number is not set in Manufacturing Order. Please set Lot/Serial Number first!"))
        return super(MrpWorkorder, self).button_start(bypass)