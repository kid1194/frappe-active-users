# Active Users © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import frappe

from active_users.utils.common import (
    _SETTINGS_,
    settings,
    clear_document_cache
)
from .migrate import after_migrate


def after_install():
    clear_document_cache(_SETTINGS_)
    frappe.clear_cache()
    
    doc = settings(True)
    
    if frappe.db.exists("User Type", "System User"):
        doc.append("user_types", {"user_type": "System User"})
    
    roles = frappe.get_all(
        "Role",
        fields=["name"],
        filters={
            "name": ["in", ["Administrator", "System Manager"]],
        },
        pluck="name"
    )
    if roles:
        if doc.roles:
            doc.roles.clear()
        
        for r in roles:
            doc.append("roles", {"role": r})
    
    doc.save(ignore_permissions=True)
        
    after_migrate()