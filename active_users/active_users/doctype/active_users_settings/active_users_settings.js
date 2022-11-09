/*
*  Active Users © 2022
*  Author:  Ameen Ahmed
*  Company: Level Up Marketing & Software Development Services
*  Licence: Please refer to license.txt
*/

frappe.provide('frappe._active_users');

frappe.ui.form.on('Active Users Settings', {
    refresh: function(frm) {
        frm.get_field('update_note').$wrapper.html(
            cint(frm.doc.has_update)
            ? '<span class="font-weight-bold text-danger">A new version is available</span>'
            : '<span class="text-muted">No new version is found</span>'
        );
    },
    check_for_update: function(frm) {
        if (frappe._active_users._init)
            frappe._active_users._init.request(
                'check_for_update',
                function(ret) {
                    if (ret) frm.reload_doc();
                }
            );
    },
    after_save: function(frm) {
        if (frappe._active_users._init)
            frappe._active_users._init.update_settings();
    }
});