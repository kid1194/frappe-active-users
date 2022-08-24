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