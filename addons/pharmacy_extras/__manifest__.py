
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
        "views/dashboard_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pharmacy_extras/static/src/js/prescription_warning.js",
        ],
        "web.assets_backend": [
            "pharmacy_extras/static/src/js/dashboard.js",
            "pharmacy_extras/static/src/xml/dashboard.xml",
        ],
    },
    "installable": True,
    "application": False,
}