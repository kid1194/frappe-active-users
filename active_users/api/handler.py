# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import frappe
from frappe.utils import cint, has_common, get_datetime_str, get_timedelta, now, now_datetime, add_to_date


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
        hidden_from_users = settings.hidden_from_listed_users
        in_users = user in users
        if (
            (not hidden_from_users and not in_users) or
            (hidden_from_users and in_users)
        ):
            frappe.cache().hset(_CACHE_KEY, cache_key, result)
            return result
        
        is_visible = True
    
    if not is_visible:
        roles = [v.role for v in settings.roles]
        if roles:
            hidden_from_roles = settings.hidden_from_listed_roles
            in_roles = has_common(roles, frappe.get_roles())
            if (
                (not hidden_from_roles and not in_roles) or
                (hidden_from_roles and in_roles)
            ):
                frappe.cache().hset(_CACHE_KEY, cache_key, result)
                return result
    
    result["is_enabled"] = True
    result["refresh_interval"] = cint(settings.refresh_interval)
    frappe.cache().hset(_CACHE_KEY, cache_key, result)
    
    return result


@frappe.whitelist()
def get_users():
    hours = 0
    minutes = 20
    seconds = 0
    
    session_expiry = frappe.db.get_value("System Settings", None, "session_expiry")
    
    if not session_expiry or not isinstance(session_expiry, str):
        session_expiry = frappe.db.get_value("System Settings", None, "session_expiry_mobile")
    
    if session_expiry and isinstance(session_expiry, str):
        session_expiry = session_expiry.split(":")
        expiry_len = len(session_expiry)
        if expiry_len > 0:
            hours = cint(session_expiry[0])
        if expiry_len > 1:
            minutes = cint(session_expiry[1])
        if expiry_len > 2:
            seconds = cint(session_expiry[2])
    
    end = now()
    start = add_to_date(end, hours=-abs(hours), minutes=-abs(minutes), seconds=-abs(seconds), as_string=True, as_datetime=True)
    doc = frappe.qb.DocType("User")
    data = (
        frappe.qb.from_(doc)
        .select(doc.name, doc.full_name, doc.user_image)
        .where(doc.enabled == 1)
        .where(doc.user_type != "Website User")
        .where(doc.last_active.between(start, end))
        .orderby(doc.full_name)
    ).run(as_dict=True)
    
    return {"users": data}