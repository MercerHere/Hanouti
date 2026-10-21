
{
    "name": "Pharmacy Extras",
    "version": "18.0.1.0.0",
    "summary": "Pharmacy-specific extensions for Odoo Inventory and POS",
    "category": "Inventory",
    "author": "Akrem Njahi",
    "license": "LGPL-3",
    "depends": ["stock", "product_expiry", "point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "views/product_views.xml",
        "views/stock_lot_views.xml",
        "views/writeoff_views.xml",
    ],
    "installable": True,
    "application": False,
}