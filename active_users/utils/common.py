# Active Users © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import json

import frappe


_LOGGER = frappe.logger("active_users", file_count=50)


_SETTINGS_ = "Active Users Settings"
_CACHE_ = "Active Users"
_CACHE_INTERVAL_ = 10

def error(msg, throw=True):
    frappe.log_error("Active Users", msg)
    if throw:
        frappe.throw(msg, title="Active Users")


def log_error(data):
    if _LOGGER:
        _LOGGER.error(data)


def get_cache(dt, key):
    return frappe.cache().hget(dt, key)


def set_cache(dt, key, data):
    frappe.cache().hset(dt, key, data)


def del_cache(dt, key):
    frappe.cache().hdel(dt, key)


def clear_cache(dt):
    frappe.cache().delete_key(dt)


def clear_document_cache(dt, name=None):
    if name is None:
        name = dt
    
    frappe.clear_cache(doctype=dt)
    frappe.clear_document_cache(dt, name)
    clear_cache(dt)


def get_cached_doc(dt, name=None, for_update=False):
    if name is None:
        name = dt
    elif isinstance(name, bool):
        for_update = name
        name = dt
    
    if for_update:
        clear_document_cache(dt)
    
    return frappe.get_cached_doc(dt, name, for_update=for_update)


def settings(for_update=False):
    return get_cached_doc(_SETTINGS_, for_update)


def parse_json(data, default=None):
    if default is None:
        default = data
    
    try:
        return json.loads(data)
    except Exception:
        return default