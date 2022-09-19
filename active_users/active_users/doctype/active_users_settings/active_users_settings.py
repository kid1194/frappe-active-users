# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import frappe
from frappe.model.document import Document

from active_users.api.handler import _SETTINGS_CACHE_KEY


class ActiveUsersSettings(Document):
	def before_save(self):
	    frappe.cache().hdel(_SETTINGS_CACHE_KEY, frappe.session.user)
