# Copyright 2023 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo.addons.mrp.tests.common import TestMrpCommon
from odoo.tests import Form


class TestMrpWorkorderPrintLabel(TestMrpCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        product_category_all = cls.env.ref("product.product_category_all")
        cls.print_label_product = cls.env["product.product"].create(
            {
                "name": "Print custom label",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "type": "product",
                "tracking": "serial",
                "categ_id": product_category_all.id,
            }
        )
        cls.component_product = cls.env["product.product"].create(
            {
                "name": "Component serial",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "type": "product",
                "tracking": "serial",
                "categ_id": product_category_all.id,
            }
        )
        cls.print_label_product_bom = cls.env["mrp.bom"].create(
            {
                "product_id": cls.print_label_product.id,
                "product_tmpl_id": cls.print_label_product.product_tmpl_id.id,
                "product_uom_id": cls.uom_unit.id,
                "product_qty": 1.0,
                "type": "normal",
                "bom_line_ids": [
                    (0, 0, {"product_id": cls.component_product.id, "product_qty": 1.0})
                ],
                "operation_ids": [
                    (0, 0, {"name": "Assemble", "workcenter_id": cls.workcenter_1.id})
                ],
            }
        )
        cls.standard_zpl_report_template = cls.env.ref("stock.label_lot_template_view")
        cls.standard_zpl_report = cls.env.ref("stock.label_lot_template")
        custom_report_arch = """<?xml version="1.0"?>
<t t-name="stock.label_lot_template_view">
            <t t-foreach="docs" t-as="lot">
                <t t-translation="off">
^XA
^A0N,44,33^FDLN/SN: <t t-esc="lot.name"/>^FS
^XZ
                </t>
            </t>
        </t>"""
        cls.custom_zpl_report_template = cls.standard_zpl_report_template.copy(
            {"key": "custom.zpl_label", "arch_base": custom_report_arch}
        )
        cls.custom_zpl_report = cls.standard_zpl_report.copy(
            {"report_name": "custom.zpl_label"}
        )
        print_label_test_type = cls.env.ref("mrp_workorder.test_type_print_label")
        cls.standard_report_quality_point = cls._create_quality_point(
            cls.print_label_product_bom.operation_ids,
            "Standard label",
            print_label_test_type,
            "zpl",
            cls.standard_zpl_report,
        )
        cls.custom_report_quality_point = cls._create_quality_point(
            cls.print_label_product_bom.operation_ids,
            "Custom label",
            print_label_test_type,
            "zpl",
            cls.custom_zpl_report,
        )
        # TODO: Add stock?

    @classmethod
    def _create_quality_point(cls, operation, name, test_type, report_type, report):
        quality_steps_action = operation.action_mrp_workorder_show_steps()
        quality_point_form = Form(
            cls.env[quality_steps_action["res_model"]].with_context(
                **quality_steps_action["context"]
            )
        )
        quality_point_form.title = "Print standard label"
        quality_point_form.test_type_id = test_type
        quality_point_form.test_report_type = report_type
        quality_point_form.test_report_id = report
        return quality_point_form.save()

    @classmethod
    def _create_manufacturing_order(cls, product, bom, quantity):
        mo_form = Form(cls.env["mrp.production"].with_user(cls.user_mrp_user))
        mo_form.product_id = product
        mo_form.bom_id = bom
        mo_form.product_qty = quantity
        return mo_form.save()

    def test_mrp_workorder_quality_point_print_custom_label(self):
        mo = self._create_manufacturing_order(
            self.print_label_product, self.print_label_product_bom, 2.0
        )
        mo.action_confirm()
        wo = mo.workorder_ids
        wo.button_start()
        wo.action_generate_serial()
        self.assertEqual(
            wo.current_quality_check_id.point_id, self.standard_report_quality_point
        )
        std_report_action = wo.action_print()
        self.assertEqual(std_report_action["id"], self.standard_zpl_report.id)
        self.assertEqual(
            std_report_action["report_name"], self.standard_zpl_report.report_name
        )
        self.assertEqual(
            wo.current_quality_check_id.point_id, self.custom_report_quality_point
        )
        custom_report_action = wo.action_print()
        self.assertEqual(custom_report_action["id"], self.custom_zpl_report.id)
        self.assertEqual(
            custom_report_action["report_name"], self.custom_zpl_report.report_name
        )
