# Active Users © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from frappe.utils import now
from frappe.utils.user import get_system_managers

from active_users import __version__
from active_users.utils.common import settings


def after_migrate():
    managers = get_system_managers(only_name=True)
    if managers:
        
        doc = settings(True)
        
        if (
            not doc.update_notification_sender or
            doc.update_notification_sender not in managers
        ):
            admin = "Administrator"
            doc.update_notification_sender = admin if admin in managers else managers.pop(0)
        
        receivers = None
        if doc.update_notification_receivers:
            receivers = [v.user for v in doc.update_notification_receivers]
        
        for manager in managers:
            if not receivers or manager not in receivers:
                doc.append(
                    "update_notification_receivers",
                    {"user": manager}
                )
        
        doc.latest_version = __version__
        doc.latest_check = now()
        
        doc.save(ignore_permissions=True)