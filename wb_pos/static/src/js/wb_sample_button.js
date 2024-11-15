import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { _t } from "@web/core/l10n/translation";

patch(ControlButtons.prototype, "wb_pos.WBSampleButton", {
    setup() {
        super.setup(...arguments);
        this.notification = this.env.services.notification;
    },

    /**
     * Custom Action for WB Sample Button
     */
    clickWBSampleButton() {
        // Example action for notification, you can replace this with your custom logic
        this.notification.add(_t("WB Sample Button Clicked"), {
            type: "success",
        });
        console.log("WB Sample Button was clicked!");
        // Add more logic here if necessary
    }
});










//
//odoo.define("wb_pos.WBSampleButton", function(require){
//  "use strict";
//
//     const PosComponent = require("point_of_sale.PosComponent");
//     const ProductScreen = require("point_of_sale.ProductScreen");
//     const Registries = require("point_of_sale.Registries");
//
//     class WBSampleButton patch PosComponent{
//
//     }
//
//     WBSampleButton.template = "WBSampleButton";
//     ProductScreen.addControlButton({
//         component: WBSampleButton,
//         position: ["before", "OrderlineCustomerNoteButton"],
//     });
//
//
//    Registries.Component.add(WBSampleButton);
//
//    return WBSampleButton;
//
//
//
//
//
//
//});