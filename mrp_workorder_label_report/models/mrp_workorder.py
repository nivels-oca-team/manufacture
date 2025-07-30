# Copyright 2023 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo import models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    def _get_product_label_action(self, report_type):
        test_report = self.current_quality_check_id.point_id.test_report_id
        if not test_report:
            return super()._get_product_label_action(report_type)
        qty = self._get_print_qty()
        # Return a report for automatic printing instead of the wizard
        res = test_report.report_action([self.product_id.id] * qty)
        # TODO: Check if really needed
        res["id"] = test_report.id
        return res

    def _get_lot_label_action(self, report_type):
        test_report = self.current_quality_check_id.point_id.test_report_id
        if not test_report:
            return super()._get_lot_label_action(report_type)
        qty = self._get_print_qty()
        res = test_report.report_action([self.finished_lot_id.id] * qty)
        # TODO: Check if really needed
        res["id"] = test_report.id
        return res
