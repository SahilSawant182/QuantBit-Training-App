frappe.ui.form.on("custum packing slip", {
    setup(frm) {
        frm.set_query("delivery_note", () => ({
            filters: { docstatus: 1 } 
        }));

        frm.set_query("item_code", "items", function () {
            return {
                filters: {
                    is_stock_item: 1
                }
            };
        });
    },

    delivery_note: function (frm) {

        if (!frm.doc.delivery_note) {
            return;
        }

        frappe.call({
            method: "get_customer_from_delivery_note",
            doc: frm.doc,
            args: {
                delivery_note: frm.doc.delivery_note
            },
            callback: function (r) {
                if (r.message) {
                    frm.set_value("customer_name", r.message);
                }
            }
        });

        frappe.call({
            method: "fetch_delivery_note_items",
            doc: frm.doc,
            callback() {
                frm.refresh_field("items");
            }
        });
    },

    after_save(frm) {
        frm.call({
            method: 'show_delivery_note',
            doc: frm.doc
        });
    },
    after_save(frm) {
        frm.call({
            method: 'update_delivery_note_customer',
            doc: frm.doc
        });
    }
});