# Copyright 2023 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
import json

from odoo import api, fields, models


class QualityPoint(models.Model):
    _inherit = "quality.point"

    test_report_id = fields.Many2one("ir.actions.report")
    display_test_report_id = fields.Boolean(compute="_compute_display_test_report_id")
    test_report_id_domain = fields.Char(compute="_compute_test_report_id_domain")

    @api.depends("operation_id")
    def _compute_display_test_report_id(self):
        for rec in self:
            rec.display_test_report_id = bool(rec.operation_id)

    @api.depends(
        "test_report_type",
        "product_ids.tracking",
        "operation_id.bom_id.product_tmpl_id.tracking",
    )
    def _compute_test_report_id_domain(self):
        for rec in self:
            report_type = "text" if rec.test_report_type == "zpl" else "pdf"
            qweb_report_type = "qweb-%s" % report_type
            product = (
                fields.first(rec.product_ids) or rec.operation_id.bom_id.product_tmpl_id
            )
            has_tracking = product.tracking != "none"
            if has_tracking:
                report_model = "stock.production.lot"
            else:
                report_model = "product.product"
            rec.test_report_id_domain = json.dumps(
                [("report_type", "=", qweb_report_type), ("model", "=", report_model)]
            )
