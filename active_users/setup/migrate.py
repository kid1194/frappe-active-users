# Active Users © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import frappe
from frappe.utils import now
from frappe.utils.user import get_system_managers

from active_users import __version__
from active_users.utils.common import settings


def after_migrate():
    managers = get_system_managers(only_name=True)
    if managers:
        if "Administrator" in managers:
            sender = "Administrator"
        else:
            sender = managers[0]
        
        doc = settings(True)
        doc.update_notification_sender = sender
        
        if doc.update_notification_receivers:
            doc.update_notification_receivers.clear()
        
        for manager in managers:
            doc.append(
                "update_notification_receivers",
                {"user": manager}
            )
        
        doc.latest_version = __version__
        doc.latest_check = now()
        
        doc.save(ignore_permissions=True)