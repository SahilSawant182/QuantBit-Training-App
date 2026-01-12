
import frappe
from frappe.model.document import Document


class DemoDoctype(Document):
	def before_save(self):
		if(self.select_any_lable=="completed"):
			frappe.msgprint("The form is copleated!")
		else:
			frappe.msgprint("The form is Pending!!!")


	def before_submit(self):
		doc = frappe.get_doc("Demo Doctype",self.name)
		frappe.msgprint(str(doc))
 
