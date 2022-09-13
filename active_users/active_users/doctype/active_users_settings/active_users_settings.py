# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt

import frappe
from frappe.model.document import Document

from active_users.api.handler import _CACHE_KEY


class ActiveUsersSettings(Document):
	def after_save(self):
	    frappe.cache().hdel(_CACHE_KEY, 'settings')
