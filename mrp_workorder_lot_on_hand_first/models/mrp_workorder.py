# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    display_lots_on_hand_first = fields.Boolean(
        related="production_id.display_lots_on_hand_first"
    )
