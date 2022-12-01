# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from frappe.model.document import Document

from active_users.utils.common import clear_document_cache


class ActiveUsersSettings(Document):
    def before_save(self):
        clear_document_cache(self.doctype)