from datetime import datetime, timedelta

import pytz

from odoo import api, fields, models
from odoo.tools.misc import formatLang


class PharmacyDashboard(models.AbstractModel):
    _name = "pharmacy.dashboard"
    _description = "Pharmacy Dashboard Data"

    @api.model
    def get_data(self):
        data = {}
        data.update(self._sales_data())
        data.update(self._expiry_data())
        data.update(self._low_stock_data())
        return data

    @api.model
    def _sales_data(self):
        tz = pytz.timezone(self.env.user.tz or "UTC")
        start_local = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
        start = start_local.astimezone(pytz.utc).replace(tzinfo=None)
        orders = self.env["pos.order"].search([
            ("date_order", ">=", start),
            ("state", "in", ["paid", "done", "invoiced"]),
        ])
        total = sum(orders.mapped("amount_total"))
        currency = self.env.company.currency_id
        return {
            "sales_total": formatLang(self.env, total, currency_obj=currency),
            "orders_count": len(orders),
        }

    @api.model
    def _expiry_data(self):
        now = fields.Datetime.now()
        Lot = self.env["stock.lot"]
        base = [("expiration_date", "!=", False), ("product_qty", ">", 0)]
        expired = Lot.search_count(base + [("expiration_date", "<", now)])
        soon_30 = Lot.search_count(base + [
            ("expiration_date", ">=", now),
            ("expiration_date", "<=", now + timedelta(days=30)),
        ])
        upcoming = Lot.search(
            base + [("expiration_date", "<=", now + timedelta(days=60))],
            order="expiration_date asc",
            limit=8,
        )
        rows = [{
            "id": lot.id,
            "product": lot.product_id.display_name,
            "lot": lot.name,
            "qty": lot.product_qty,
            "date": lot.expiration_date.date().isoformat(),
            "days_left": (lot.expiration_date - now).days,
        } for lot in upcoming]
        return {"expired_count": expired, "soon_count": soon_30, "expiring": rows}

    @api.model
    def _low_stock_data(self):
        rows = []
        for op in self.env["stock.warehouse.orderpoint"].search([]):
            on_hand = op.product_id.with_context(
                location=op.location_id.id
            ).qty_available
            if on_hand < op.product_min_qty:
                rows.append({
                    "id": op.id,
                    "product": op.product_id.display_name,
                    "on_hand": on_hand,
                    "min": op.product_min_qty,
                })
        rows.sort(key=lambda r: r["on_hand"])
        return {"low_stock_count": len(rows), "low_stock": rows[:8]}