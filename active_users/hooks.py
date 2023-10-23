# Active Users © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from .version import __frappe_version_min_14__


app_name = "active_users"
app_title = "Active Users"
app_publisher = "Ameen Ahmed (Level Up)"
app_description = "Frappe plugin that displays a list of current active users."
app_icon = "octicon octicon-person"
app_color = "blue"
app_email = "kid1194@gmail.com"
app_license = "MIT"


app_include_css = [
    "active_users.bundle.css"
] if __frappe_version_min_14__ else [
    "/assets/active_users/css/active_users.css"
]
app_include_js = [
    "active_users.bundle.js"
] if __frappe_version_min_14__ else [
    "/assets/active_users/js/active_users.js"
]


after_install = "active_users.setup.install.after_install"
after_migrate = "active_users.setup.migrate.after_migrate"


scheduler_events = {
    "daily": [
        "active_users.utils.update.auto_check_for_update"
    ]
}