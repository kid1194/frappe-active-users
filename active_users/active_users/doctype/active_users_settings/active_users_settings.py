# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import frappe
from frappe.model.document import Document

from active_users.utils import clear_document_cache, compare_versions
from active_users import __version__


class ActiveUsersSettings(Document):
    @property
    def has_update(self):
        return 1 if compare_versions(self.latest_version, __version__) > 0 else 0
    
    
	def before_save(self):
	    clear_document_cache(self.doctype)
