from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockLot(models.Model):
    _inherit = "stock.lot"

    pharmacy_expiry_notified = fields.Boolean(
        string="Expiry Alert Sent", default=False, copy=False
    )

    @api.model
    def _cron_pharmacy_expiry_alert(self):
        """Create a to-do for stock managers for each in-stock lot that is
        expired or expires within the configured number of days."""
        days = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("pharmacy_extras.expiry_alert_days", 60)
        )
        now = fields.Datetime.now()
        lots = self.search([
            ("expiration_date", "!=", False),
            ("expiration_date", "<=", now + timedelta(days=days)),
            ("product_qty", ">", 0),
            ("pharmacy_expiry_notified", "=", False),
        ])
        managers = self.env.ref("stock.group_stock_manager").users.filtered("active")
        assignee = managers[:1] or self.env.ref("base.user_admin")
        for lot in lots:
            if lot.expiration_date < now:
                summary = _("Expired: %s", lot.display_name)
            else:
                summary = _("Expiring soon: %s", lot.display_name)
            lot.activity_schedule(
                "mail.mail_activity_data_todo",
                summary=summary,
                note=_(
                    "%(product)s, lot %(lot)s, expires %(date)s, %(qty)s on hand.",
                    product=lot.product_id.display_name,
                    lot=lot.name,
                    date=lot.expiration_date,
                    qty=lot.product_qty,
                ),
                user_id=assignee.id,
            )
            lot.pharmacy_expiry_notified = True
        return len(lots)
    def action_dispose_expired(self):
        now = fields.Datetime.now()
        expired = self.filtered(lambda l: l.expiration_date and l.expiration_date < now)
        if not expired:
            raise UserError(_("None of the selected lots has expired."))
        disposed = 0
        for lot in expired:
            quants = self.env["stock.quant"].search([
                ("lot_id", "=", lot.id),
                ("location_id.usage", "=", "internal"),
            ])
            for quant in quants:
                qty = quant.quantity - quant.reserved_quantity
                if qty <= 0:
                    continue
                scrap = self.env["stock.scrap"].create({
                    "product_id": quant.product_id.id,
                    "lot_id": lot.id,
                    "scrap_qty": qty,
                    "product_uom_id": quant.product_id.uom_id.id,
                    "location_id": quant.location_id.id,
                    "origin": _("Expired stock disposal"),
                })
                scrap.action_validate()
                self.env["pharmacy.writeoff"].create({
                    "lot_id": lot.id,
                    "product_id": quant.product_id.id,
                    "quantity": qty,
                    "location_id": quant.location_id.id,
                    "expiration_date": lot.expiration_date,
                    "scrap_id": scrap.id,
                })
                disposed += 1
        if not disposed:
            raise UserError(_("No available stock to dispose (it may be reserved)."))
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Done"),
                "message": _("%s stock line(s) written off.", disposed),
                "type": "success",
            },
        }