/*
*  Active Users © 2022
*  Author:  Ameen Ahmed
*  Company: Level Up Marketing & Software Development Services
*  Licence: Please refer to license.txt
*/

frappe.provide('frappe._active_users');

frappe.ui.form.on('Active Users Settings', {
    after_save: function(frm) {
        if (frappe._active_users.update_settings) {
            frappe._active_users.update_settings();
        }
    }
});