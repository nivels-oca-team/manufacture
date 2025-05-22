# Copyright 2023 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
{
    "name": "MRP Workorder Label Report",
    "summary": "Use specific label report for workorders on quality points",
    "version": "17.0.24.12.1",
    "category": "Manufacturing/Manufacturing",
    "website": "https://github.com/camptocamp/odoo-enterprise-addons",
    "author": "Camptocamp",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mrp_workorder",
        # "web_domain_field"
    ],
    "data": [
        "views/quality_point.xml"
    ],
}
