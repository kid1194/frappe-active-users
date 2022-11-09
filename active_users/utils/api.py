# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


import json
import re

import frappe
from frappe import _dict
from frappe.utils import (
    cint,
    has_common,
    now,
    add_to_date
)

from .common import _SETTINGS_, settings, get_cache, set_cache, log_error


@frappe.whitelist()
def get_settings():
    user = frappe.session.user
    cache = get_cache(_SETTINGS_, user)
    
    if cache and isinstance(cache, dict):
        return cache
    
    result = _dict({
        "enabled": 0,
        "refresh_interval": 5,
        "allow_manual_refresh": 0
    })
    status = 0
    app = settings()
    
    if not cint(app.enabled):
        status = 2
    
    if not status and app.users:
        users = [v.user for v in app.users]
        if users and user in users:
            status = 2 if cint(app.hidden_from_listed_users) else 1
    
    if not status and app.roles:
        roles = [v.role for v in app.roles]
        if roles and has_common(roles, frappe.get_roles()):
            status = 2 if cint(app.hidden_from_listed_roles) else 1
            
    if status == 1:
        result.enabled = 1
        result.refresh_interval = cint(app.refresh_interval)
        result.allow_manual_refresh = 1 if cint(app.allow_manual_refresh) else 0
    
    set_cache(_SETTINGS_, user, result)
    return result


@frappe.whitelist()
def get_users():
    app = settings()
    user_types = [v.user_type for v in app.user_types]
    tp = [0, -20, 0]
    
    sess_expiry = frappe.get_system_settings("session_expiry")
    if not sess_expiry or not isinstance(sess_expiry, str):
        sess_expiry = frappe.get_system_settings("session_expiry_mobile")
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
                return {"error": 1, "message": "The system session expiry value is invalid."}
    except Exception as exc:
        log_error(exc)
        return {"error": 1, "message": "Unable to parse the system session expiry value."}
    
    end = now()
    start = add_to_date(end, hours=tp[0], minutes=tp[1], seconds=tp[2], as_string=True, as_datetime=True)
    
    try:
        data = frappe.get_all(
            "User",
            fields=["name", "full_name", "user_image"],
            filters={
                "enabled": 1,
                "user_type": ["in", user_types],
                "last_active": ["between", [start, end]],
            },
            order_by="full_name asc",
            limit_page_length=0,
        )
        return {"users": data}
    except Exception as exc:
        log_error(exc)
        return {"error": 1, "message": "Unable to get the list of active users."}