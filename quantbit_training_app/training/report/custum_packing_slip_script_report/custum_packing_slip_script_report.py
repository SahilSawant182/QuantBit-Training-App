# Copyright (c) 2026, Sahil-Sawant and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {
            'fieldname': 'packing_slip',
            'label': _('Packing Slip'),
            'fieldtype': 'Link',
            'options': 'custum packing slip'
        },
        {
            'fieldname': 'customer_name',
            'label': _('Customer'),
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'delivery_note',
            'label': _('Delivery Note'),
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'item_code',
            'label': _('Item Code'),
            'fieldtype': 'Link',
            'options': 'Item'
        },
        {
            'fieldname': 'item_name',
            'label': _('Item Name'),
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'qty',
            'label': _('Qty'),
            'fieldtype': 'Float'
        }
    ]

    data = frappe.db.sql("""
        SELECT
            cps.name AS packing_slip,
            cps.customer_name,
            cps.delivery_note,
            cpsi.item_code,
            cpsi.item_name,
            cpsi.qty
        FROM `tabcustum packing slip` cps
        JOIN `tabPacking Slip Item` cpsi
            ON cps.name = cpsi.parent
        WHERE cps.docstatus < 2
        ORDER BY cps.creation DESC
    """, as_dict=True)

    return columns, data