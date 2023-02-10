# Active Users © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from frappe.model.document import Document

from active_users.utils.common import (
    _CACHE_,
    _CACHE_INTERVAL_,
    clear_document_cache,
    del_cache,
    clear_cache
)


class ActiveUsersSettings(Document):
    def before_save(self):
        clear_document_cache(self.doctype)
        if self.refresh_interval < _CACHE_INTERVAL_:
            clear_cache(_CACHE_)
        else:
            del_cache(_CACHE_, "settings")