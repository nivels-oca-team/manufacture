# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "MRP Workorder Lock Planning",
    "summary": "Lock the planning of a MRP workorder to avoid rescheduling",
    "version": "17.0.1.0.1",
    "development_status": "Beta",
    "category": "Manufacturing/Manufacturing",
    "website": "https://github.com/OCA/manufacture",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["grindtildeath"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mrp",
        "mrp_workorder"
    ],
    "data": [
        "views/mrp_workorder.xml",
    ],
}
