# Active Users © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt


from frappe import _


def get_data():
    return [
        {
            "module_name": "Active Users",
            "color": "blue",
            "icon": "octicon octicon-person",
            "type": "module",
            "label": _("Active Users")
        }
    ]