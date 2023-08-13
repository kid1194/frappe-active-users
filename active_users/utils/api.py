# Active Users © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import json
import re

import frappe
from frappe import _dict
from frappe.utils import (
    cint,
    has_common,
    now,
    add_to_date,
    get_datetime,
    now_datetime
)

from .common import (
    _SETTINGS_,
    _CACHE_,
    _CACHE_INTERVAL_,
    settings,
    get_cache,
    set_cache,
    del_cache,
    log_error
)


@frappe.whitelist()
def get_settings():
    cache_key = "settings"
    cache = get_cache(_CACHE_, cache_key)
    
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
        if users and frappe.session.user in users:
            status = 2 if cint(app.hidden_from_listed_users) else 1
    
    if not status and app.roles:
        roles = [v.role for v in app.roles]
        if roles and has_common(roles, frappe.get_roles()):
            status = 2 if cint(app.hidden_from_listed_roles) else 1
            
    if status == 1:
        result.enabled = 1
        result.refresh_interval = cint(app.refresh_interval)
        result.allow_manual_refresh = 1 if cint(app.allow_manual_refresh) else 0
    
    set_cache(_CACHE_, cache_key, result)
    return result


@frappe.whitelist()
def get_users():
    app = settings()
    
    if not cint(app.enabled):
        return {"users": []}
    
    cache_key = "users"
    
    if app.refresh_interval >= _CACHE_INTERVAL_:
        cache = get_cache(_CACHE_, cache_key)
        
        if cache and isinstance(cache, dict):
            if get_datetime(cache.expiry) < now_datetime():
                del_cache(_CACHE_, cache_key)
            else:
                return {"users": cache.data}
    
    
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
    
    now_dt = now()
    start = add_to_date(now_dt, hours=tp[0], minutes=tp[1], seconds=tp[2], as_string=True, as_datetime=True)
    user_types = [v.user_type for v in app.user_types]
    
    try:
        data = frappe.get_all(
            "User",
            fields=["name", "full_name", "user_image"],
            filters={
                "enabled": 1,
                "name": ["!=", frappe.session.user],
                "user_type": ["in", user_types],
                "last_active": [">=", start],
            },
            order_by="full_name asc",
            limit_page_length=0,
        )
        
        if app.refresh_interval >= _CACHE_INTERVAL_:
            set_cache(_CACHE_, cache_key, _dict({
                "data": data,
                "expiry": add_to_date(now_dt, minutes=_CACHE_INTERVAL_, as_string=True, as_datetime=True)
            }))
        
        return {"users": data}
    except Exception as exc:
        log_error(exc)
        return {"error": 1, "message": "Unable to get the list of active users."}