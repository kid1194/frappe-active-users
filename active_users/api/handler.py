# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import frappe
from frappe.utils import cint, has_common, get_datetime_str, get_timedelta, now, now_datetime


_CACHE_KEY = "active_users"


@frappe.whitelist()
def get_settings():
    cache_key = "settings"
    cache = frappe.cache().hget(_CACHE_KEY, cache_key)
    
    if isinstance(cache, dict) and "refresh_interval" in cache:
        return cache
    
    result = {
        "is_enabled": False,
        "refresh_interval": 5
    }
    
    settings = frappe.get_cached_doc("Active Users Settings")
    
    if not settings.is_enabled:
        frappe.cache().hset(_CACHE_KEY, cache_key, result)
        return result
    
    user = frappe.session.user
    users = [v.user for v in settings.users]
    is_visible = False
    if users:
        visible_for_users = settings.users_restriction == "Enabled For Listed Users"
        in_users = user in users
        if (
            (visible_for_users and not in_users) or
            (not visible_for_users and in_users)
        ):
            frappe.cache().hset(_CACHE_KEY, cache_key, result)
            return result
        
        is_visible = True
    
    if not is_visible:
        roles = [v.role for v in settings.roles]
        if roles:
            visible_for_roles = settings.roles_restriction == "Enabled For Listed Roles"
            in_roles = has_common(roles, frappe.get_roles())
            if (
                (visible_for_roles and not in_roles) or
                (not visible_for_roles and in_roles)
            ):
                frappe.cache().hset(_CACHE_KEY, cache_key, result)
                return result
    
    result["is_enabled"] = True
    result["refresh_interval"] = cint(settings.refresh_interval)
    frappe.cache().hset(_CACHE_KEY, cache_key, result)
    
    return result


@frappe.whitelist()
def get_users():
    session_expiry = frappe.db.get_value("System Settings", fieldname="session_expiry", pluck=True)
    if len(session_expiry.split(":")) < 3:
        session_expiry = session_expiry + ":00"
    
    doc = frappe.qb.DocType("User")
    start = get_datetime_str(now_datetime() - get_timedelta(session_expiry))
    end = now()
    return (
        frappe.db.from_(doc)
        .select(doc.name, doc.full_name, doc.user_image)
        .where(doc.enabled == 1)
        .where(doc.user_type != "Website User")
        .where(doc.last_active.between(start, end))
        .orderby(doc.full_name)
    ).run(as_dict=True)