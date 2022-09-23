# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import frappe

from active_users.api.handler import _SETTINGS_CACHE_KEY


def after_install():
    frappe.cache().delete_key(_SETTINGS_CACHE_KEY)
    frappe.clear_cache()
    
    settings = frappe.get_doc("Active Users Settings")
    changed = False
    
    if frappe.db.exists("User Type", "System User"):
        settings.append("user_types", {"user_type": "System User"})
        changed = True
    
    if (roles := frappe.db.get_list(
        "Role",
        fields=["name"],
        filters={
            "name": ["in", ["Administrator", "System Manager"]],
        },
        pluck="name"
    )):
        if not len([v.role for v in settings.roles if v.role in roles]):
            for r in roles:
                settings.append("roles", {"role": r})
                changed = True
        
    if changed:
        settings.save(ignore_permissions=True)