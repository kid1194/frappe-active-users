# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


from datetime import datetime

import frappe
from frappe.utils import has_common, get_datetime_str, get_timedelta, now


_CACHE_KEY = "active_users"


@frappe.whitelist()
def get_settings():
    cache_key = "settings"
    cache = frappe.cache().hget(_CACHE_KEY, cache_key)
    
    if isinstance(cache, dict):
        return cache
    
    result = {
        "is_enabled": False,
    }
    
    settings = frappe.get_cached_doc("Active Users Settings")
    
    if not settings.is_enabled:
        frappe.cache().hset(_CACHE_KEY, cache_key, result)
        return result
    
    users = [v.user for v in settings.users]
    visible_for_users = settings.users_condition == "Visible Only For Listed Users"
    if (
        (
            visible_for_users and user not in users
        ) or (
            not visible_for_users and user in users
        )
    ):
        frappe.cache().hset(_CACHE_KEY, cache_key, result)
        return result
    
    roles = [v.role for v in settings.roles]
    visible_for_roles = settings.roles_condition == "Visible Only For Listed Roles"
    if (
        (
            visible_for_roles and not has_common(roles, frappe.get_roles())
        ) or (
            not visible_for_roles and has_common(roles, frappe.get_roles())
        )
    ):
        frappe.cache().hset(_CACHE_KEY, cache_key, result)
        return result
    
    result["is_enabled"] = True
    result["refresh_interval"] = settings.refresh_interval
    frappe.cache().hset(_CACHE_KEY, cache_key, result)
    return result


@frappe.whitelist()
def get_users():
    session_expiry = frappe.db.get_value("System Settings", fieldname="session_expiry", pluck=True)
    doc = frappe.qb.DocType("User")
    start = get_datetime_str(datetime(now()) - get_timedelta(session_expiry))
    end = now()
    return (
        frappe.db.from_(doc)
        .select(doc.name, doc.full_name, doc.user_image)
        .where(doc.last_active.between(start, end))
    ).run(as_dict=True)
