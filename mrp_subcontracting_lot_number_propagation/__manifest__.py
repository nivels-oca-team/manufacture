# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "MRP Serial Number Propagation (subcontracting)",
    "version": "17.0.1.0.1",
    "development_status": "Beta",
    "license": "AGPL-3",
    "author": "Camptocamp, Odoo Community Association (OCA), nivels Gmbh",
    "maintainers": ["nivels"],
    "summary": (
        "Propagate a serial number from a component to a finished product "
        "(subcontracting integration)"
    ),
    "website": "https://github.com/OCA/manufacture",
    "category": "Manufacturing",
    "depends": [
        # core
        "mrp",
        "mrp_subcontracting",
        # OCA/manufacture
        "mrp_lot_number_propagation",
    ],
    "data": [
        "views/stock_move_line.xml",
        'views/mrp_produciton_view.xml'
    ],
    "installable": True,
    "auto_install": True,
    "application": False,
}
