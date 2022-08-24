# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import frappe


def after_install():
    roles = frappe.db.get_list(
        "Role",
        fields=["name"],
        filters={
            "name": ["in", ["Administrator", "System Manager"]],
        },
        pluck="name"
    )
    
    if roles:
        settings = frappe.get_doc("Active Users Settings")
        
        for r in roles:
            settings.append("roles", {"role": r})
        
        settings.save(ignore_permissions=True)