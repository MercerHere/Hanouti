# Hanouti

Hanouti is an Odoo-based project focused on pharmacy and POS operations.  
This repository currently ships a custom Odoo add-on: `pharmacy_extras`.

## What it adds

- **Prescription-aware POS flow**: warns cashiers before adding products marked as prescription-only.
- **Expiry monitoring**: scheduled alerts for lots that are expired or approaching expiry.
- **Expired stock disposal**: bulk write-off action for expired lots with audit records.
- **Pharmacy dashboard**: inventory and sales KPIs (sales today, expiring lots, low-stock products).

## Repository layout

- `/addons/pharmacy_extras` — custom Odoo module code (models, views, assets, security, data).
- `/docker-compose.yml` — local Odoo + PostgreSQL stack, with `./addons` mounted as extra add-ons.

## Minimal local run

1. Create a `.env` file with `DB_PASSWORD`.
2. Start the stack with Docker Compose.
3. In Odoo, install the **Pharmacy Extras** module (`pharmacy_extras`).

