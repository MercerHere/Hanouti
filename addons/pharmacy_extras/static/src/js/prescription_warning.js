/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { ask } from "@point_of_sale/app/store/make_awaitable_dialog";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async addLineToCurrentOrder(vals, opts = {}, configure = true) {
        const product = vals.product_id;
        if (product && product.prescription_required) {
            const confirmed = await ask(this.dialog, {
                title: _t("Prescription required"),
                body: _t(
                    "%s can only be sold with a valid prescription. Has the customer presented one?",
                    product.display_name
                ),
                confirmLabel: _t("Yes, add to order"),
                cancelLabel: _t("Cancel"),
            });
            if (!confirmed) {
                return;
            }
        }
        return super.addLineToCurrentOrder(vals, opts, configure);
    },
});