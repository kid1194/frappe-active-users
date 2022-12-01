# Active Users © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import frappe

from .common import _SETTINGS_, del_cache


def on_login(login_manager):
    del_cache(_SETTINGS_, login_manager.user)


def on_logout(login_manager):
    del_cache(_SETTINGS_, frappe.session.user)