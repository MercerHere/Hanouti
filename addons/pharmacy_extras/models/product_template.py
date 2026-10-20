from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    prescription_required = fields.Boolean(
        string="Prescription Required",
        help="Check if this product can only be sold with a prescription.",
    )