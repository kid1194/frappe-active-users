# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import frappe
from frappe.utils import cint, has_common, get_datetime_str, get_timedelta, now, now_datetime, add_to_date


_SETTINGS_CACHE_KEY = "active_users_settings"


def on_login(login_manager):
    frappe.cache().hdel(_SETTINGS_CACHE_KEY, login_manager.user)


def on_logout():
    frappe.cache().hdel(_SETTINGS_CACHE_KEY, frappe.session.user)


@frappe.whitelist()
def get_settings():
    user = frappe.session.user
    cache = frappe.cache().hget(_SETTINGS_CACHE_KEY, user)
    if isinstance(cache, dict) and "refresh_interval" in cache:
        return cache
    
    result = {
        "is_enabled": False,
        "refresh_interval": 5
    }
    status = 0
    settings = frappe.get_doc("Active Users Settings")
    
    if not settings.is_enabled:
        status = 2
    
    if not status and settings.users:
        users = [v.user for v in settings.users]
        if users and user in users:
            status = 2 if settings.hidden_from_listed_users else 1
    
    if not status and settings.roles:
        roles = [v.role for v in settings.roles]
        if roles and has_common(roles, frappe.get_roles()):
            status = 2 if settings.hidden_from_listed_roles else 1
            
    if status == 1:
        result["is_enabled"] = True
        result["refresh_interval"] = cint(settings.refresh_interval)
    
    frappe.cache().hset(_SETTINGS_CACHE_KEY, user, result)
    return result


@frappe.whitelist()
def get_users():
    tp = [0, -20, 0]
    sess_expiry = frappe.db.get_value("System Settings", None, "session_expiry")
    
    if not sess_expiry or not isinstance(sess_expiry, str):
        sess_expiry = frappe.db.get_value("System Settings", None, "session_expiry_mobile")
    
    if sess_expiry and isinstance(sess_expiry, str):
        sess_expiry = sess_expiry.split(":")
        for i in range(len(sess_expiry)):
            tp[i] = cint(sess_expiry[i])
            if tp[i]:
                tp[i] = -abs(tp[i])
    
    end = now()
    start = add_to_date(end, hours=tp[0], minutes=tp[1], seconds=tp[2], as_string=True, as_datetime=True)
    
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