# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import frappe
from frappe.utils import cint, has_common, get_datetime_str, get_timedelta, now, now_datetime, add_to_date


logger = frappe.logger("active-users", file_count=50)


_SETTINGS_CACHE_KEY = "active_users_settings"


@frappe.whitelist()
def get_settings():
    user = frappe.session.user
    cache = frappe.cache().hget(_SETTINGS_CACHE_KEY, user)
    
    if isinstance(cache, dict) and "refresh_interval" in cache:
        logger.debug({"message": "Returning cached settings", "user": user, "data": cache})
        return cache
    
    result = {
        "is_enabled": False,
        "refresh_interval": 5
    }
    
    settings = frappe.get_doc("Active Users Settings")
    
    if not settings.is_enabled:
        logger.debug({"message": "Plugin not enabled", "user": user, "data": result})
        frappe.cache().hset(_SETTINGS_CACHE_KEY, user, result)
        return result
    
    users = [v.user for v in settings.users]
    if users:
        hidden_from_users = settings.hidden_from_listed_users == 1
        in_users = user in users
        logger.debug({"message": "Checking users visibility", "listed_users": users, "to_be_hidden", hidden_from_users, "data": result})
        
        if (
            (not hidden_from_users and not in_users) or
            (hidden_from_users and in_users)
        ):
            logger.debug({"message": "Hidden from user", "user": user, "data": result})
            frappe.cache().hset(_SETTINGS_CACHE_KEY, user, result)
            return result
    
    if not users:
        roles = [v.role for v in settings.roles]
        if roles:
            hidden_from_roles = settings.hidden_from_listed_roles == 1
            in_roles = has_common(roles, frappe.get_roles())
            logger.debug({"message": "Checking roles visibility", "listed_roles": roles, "to_be_hidden", hidden_from_roles, "data": result})
            
            if (
                (not hidden_from_roles and not in_roles) or
                (hidden_from_roles and in_roles)
            ):
                logger.debug({"message": "Hidden from roles", "roles": frappe.get_roles(), "data": result})
                frappe.cache().hset(_SETTINGS_CACHE_KEY, user, result)
                return result
    
    result["is_enabled"] = True
    result["refresh_interval"] = cint(settings.refresh_interval)
    frappe.cache().hset(_SETTINGS_CACHE_KEY, user, result)
    logger.debug({"message": "Plugin is enabled and visible", "user": user, "data": result})
    return result


@frappe.whitelist()
def get_users():
    hours = 0
    minutes = 20
    seconds = 0
    
    session_expiry = frappe.db.get_value("System Settings", None, "session_expiry")
    logger.debug({"message": "Getting session expiry from system settings", "data": session_expiry})
    
    if not session_expiry or not isinstance(session_expiry, str):
        session_expiry = frappe.db.get_value("System Settings", None, "session_expiry_mobile")
        logger.debug({"message": "Getting mobile session expiry from system settings", "data": session_expiry})
    
    if session_expiry and isinstance(session_expiry, str):
        session_expiry = session_expiry.split(":")
        expiry_len = len(session_expiry)
        if expiry_len > 0:
            hours = cint(session_expiry[0])
        if expiry_len > 1:
            minutes = cint(session_expiry[1])
        if expiry_len > 2:
            seconds = cint(session_expiry[2])
        logger.debug({"message": "Parsing session expiry", "data": [hours, minutes, seconds]})
    
    end = now()
    start = add_to_date(end, hours=-abs(hours), minutes=-abs(minutes), seconds=-abs(seconds), as_string=True, as_datetime=True)
    logger.debug({"message": "Users last active time span", "data": {"start": start, "end": end}})
    
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