# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2019 Rubén Bravo <rubenred18@gmail.com>
# Copyright 2020 Tecnativa - Pedro M. Baeza
##############################################################################
#
# Nivels GmbH
# Comercialstrasse 19
# 7000 Chur
#
# Copyright (C) 2020 Nivels GmbH.
# All Rights Reserved
#
##############################################################################
{
    "name": "MRP Sale Info",
    "summary": "Adds sale information to Manufacturing models",
    "version": "17.0.1.2.0",
    "category": "Manufacturing",
    "website": "https://github.com/OCA/manufacture",
    "author": "AvanzOSC, Tecnativa, Odoo Community Association (OCA), nivels GmbH",
    "license": "OPL-1",
    "application": False,
    "installable": True,
    "depends": [
        "mrp",
        "sale_stock",
    ],
    "data": [
        "views/mrp_production.xml",
        "views/mrp_workorder.xml",
    ],
}
