/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class PharmacyDashboard extends Component {
    static template = "pharmacy_extras.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ data: null });
        onWillStart(() => this.load());
    }

    async load() {
        this.state.data = await this.orm.call("pharmacy.dashboard", "get_data", []);
    }

    openExpiring() {
        this.action.doAction("pharmacy_extras.action_expiring_lots");
    }

    openReordering() {
        this.action.doAction("stock.action_orderpoint");
    }
}

registry.category("actions").add("pharmacy_extras.dashboard", PharmacyDashboard);