from . import __version__ as app_version
from frappe import __version__ as frappe_version

app_name = "active_users"
app_title = "Active Users"
app_publisher = "Ameen Ahmed (Level Up)"
app_description = "Frappe plugin that displays a list of current active users."
app_icon = "octicon octicon-person"
app_color = "blue"
app_email = "kid1194@gmail.com"
app_license = "MIT"
is_frappe_above_v13 = int(frappe_version.split('.')[0]) > 13

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/active_users/css/select.css"
# app_include_js = "/assets/active_users/js/select.js"

app_include_css = ['active_users.bundle.css'] if is_frappe_above_v13 else ['/assets/active_users/css/active_users.css']
app_include_js = ['active_users.bundle.js'] if is_frappe_above_v13 else ['/assets/active_users/js/active_users.js']

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "active_users/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "active_users.utils.jinja_methods",
# 	"filters": "active_users.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "active_users.install.before_install"
after_install = "active_users.setup.install.after_install"

# login
on_login = ["active_users.api.handler.on_login"]
on_logout = ["active_users.api.handler.on_logout"]

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "active_users.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"active_users.tasks.all"
# 	],
# 	"daily": [
# 		"active_users.tasks.daily"
# 	],
# 	"hourly": [
# 		"active_users.tasks.hourly"
# 	],
# 	"weekly": [
# 		"active_users.tasks.weekly"
# 	],
# 	"monthly": [
# 		"active_users.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "active_users.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "active_users.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "active_users.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"active_users.auth.validate"
# ]

