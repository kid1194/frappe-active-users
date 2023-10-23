# Active Users © 2023
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from frappe import __version__ as frappe_version


__frappe_version__ = int(frappe_version.split(".")[0])
__frappe_version_min_15__ = __frappe_version__ > 14
__frappe_version_min_14__ = __frappe_version__ > 13