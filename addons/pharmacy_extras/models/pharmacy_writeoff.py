from odoo import fields, models


class PharmacyWriteoff(models.Model):
    _name = "pharmacy.writeoff"
    _description = "Expired Stock Write-off"
    _order = "date desc, id desc"

    lot_id = fields.Many2one("stock.lot", string="Lot", required=True, readonly=True)
    product_id = fields.Many2one("product.product", required=True, readonly=True)
    quantity = fields.Float(required=True, readonly=True)
    location_id = fields.Many2one("stock.location", string="Location", readonly=True)
    expiration_date = fields.Datetime(readonly=True)
    date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one(
        "res.users", string="Done By", default=lambda self: self.env.user, readonly=True
    )
    reason = fields.Selection(
        [("expired", "Expired")], default="expired", required=True, readonly=True
    )
    scrap_id = fields.Many2one("stock.scrap", string="Scrap Order", readonly=True)