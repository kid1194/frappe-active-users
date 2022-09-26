# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import json

import frappe
from frappe.utils import cint, has_common, now, add_to_date


_SETTINGS_CACHE_KEY = "active_users_settings"
_SETTINGS_DOCTYPE = "Active Users Settings"


def on_login(login_manager):
    frappe.cache().hdel(_SETTINGS_CACHE_KEY, login_manager.user)


def on_logout():
    frappe.cache().hdel(_SETTINGS_CACHE_KEY, frappe.session.user)


@frappe.whitelist()
def get_settings():
    user = frappe.session.user
    cache = frappe.cache().hget(_SETTINGS_CACHE_KEY, user)
    if (
        isinstance(cache, dict) and
        "refresh_interval" in cache and
        "allow_manual_refresh" in cache
    ):
        return cache
    
    result = {
        "is_enabled": False,
        "refresh_interval": 5,
        "allow_manual_refresh": False,
    }
    status = 0
    settings = frappe.get_cached_doc(_SETTINGS_DOCTYPE, _SETTINGS_DOCTYPE)
    
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
        result["allow_manual_refresh"] = True if settings.allow_manual_refresh else False
    
    frappe.cache().hset(_SETTINGS_CACHE_KEY, user, result)
    return result


@frappe.whitelist()
def get_users():
    settings = frappe.get_cached_doc(_SETTINGS_DOCTYPE, _SETTINGS_DOCTYPE)
    user_types = [v.user_type for v in settings.user_types]
    sys_settings = frappe.get_cached_doc("System Settings", "System Settings")
    tp = [0, -20, 0]
    
    sess_expiry = sys_settings.session_expiry
    if not sess_expiry or not isinstance(sess_expiry, str):
        sess_expiry = sys_settings.session_expiry_mobile
    if not sess_expiry or not isinstance(sess_expiry, str):
        sess_expiry = ""
    
    try:
        if sess_expiry:
            sess_list = sess_expiry.split(":")
            if sess_list and not isinstance(sess_list, list):
                sess_list = [sess_list]
            if sess_list and isinstance(sess_list, list):
                idx = 0
                for v in sess_list:
                    if v and isinstance(v, str):
                        tpv = cint(v)
                        if tpv:
                            tp[idx] = -abs(tpv)
                    idx += 1
            else:
                return {"error": True, "message": "The system session expiry value is invalid."}
    except Exception:
        return {"error": True, "message": "Unable to parse the system session expiry value."}
    
    end = now()
    start = add_to_date(end, hours=tp[0], minutes=tp[1], seconds=tp[2], as_string=True, as_datetime=True)
    
    try:
        data = frappe.get_all(
            "User",
            fields=["name", "full_name", "user_image"],
            filters={
                "enabled": 1,
                "user_type": ["in", user_type],
                "last_active": ["between", [start, end]],
            },
            order_by="full_name asc",
            limit_page_length=0,
        )
        return {"users": data}
    except Exception:
        return {"error": True, "message": "Unable to get the list of active users."}