# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
{
    "name": "Mrp Workorder Lot On Hand First",
    "summary": "Allows to display lots on hand first in workorder screen",
    "version": "17.0.24.12.1",
    "category": "Manufacturing/Manufacturing",
    "website": "https://github.com/camptocamp/odoo-enterprise-addons",
    "author": "Camptocamp",
    "license": "LGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "mrp_lot_on_hand_first",
        "mrp_workorder",
    ],
    "data": [
        "views/mrp_workorder.xml",
    ],
}
