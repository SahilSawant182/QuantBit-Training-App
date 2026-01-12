

import frappe
from frappe.model.document import Document


class custumpackingslip(Document):

	@frappe.whitelist()
	def get_customer_from_delivery_note(delivery_note):
		if delivery_note:
			return frappe.db.get_value(
				'Delivery Note',
				delivery_note,
				'customer'
			)

	@frappe.whitelist()
	def fetch_delivery_note_items(self):

		if not self.delivery_note:
			return

		self.set("items", [])

		delivery_note_items = frappe.get_all(
			"Delivery Note Item",
			filters={"parent": self.delivery_note},
			fields=["item_code", "item_name", "qty"]
		)

		for item in delivery_note_items:
			self.append("items", {
				"item_code": item.get("item_code"),
				"item_name": item.get("item_name"), 
				"qty": item.get("qty")
			})

	@frappe.whitelist()
	def show_delivery_note(self):
		if self.delivery_note:
			dn = frappe.get_doc("Delivery Note", self.delivery_note)

			frappe.msgprint(
				f"Delivery Note: {dn.name}<br>"
				f"Customer: {dn.customer}"
			)
			
	@frappe.whitelist()
	def update_delivery_note_customer(self):
		if self.delivery_note and self.customer_name:
			frappe.db.set_value(
				'Delivery Note',
				self.delivery_note,
				'customer',
				self.customer_name
			)
	
	def on_submit(self):
		dox = frappe.new_doc("Duplicate Custome Packing Slip")
		dox.delivery_note = self.delivery_note
		dox.customer_name = self.customer_name 
		dox.from_case_no = self.from_case_no
		for item in self.items:
			dox.append("items", {
				"item_code": item.item_code,
				"item_name": item.item_name,
				"qty": item.qty
			})
		dox.insert()
		dox.custom_packing_slip = self.name
		dox.submit()
		frappe.msgprint("Duplicate Packing Slip Created Successfully") 