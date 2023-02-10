/*
*  Active Users © 2023
*  Author:  Ameen Ahmed
*  Company: Level Up Marketing & Software Development Services
*  Licence: Please refer to LICENSE file
*/

frappe.provide('frappe._active_users');

frappe.ui.form.on('Active Users Settings', {
    setup: function(frm) {
        frm.AU = {
            update_messages: [
                __('No new version is found'),
                __('A new version is available'),
            ],
            update_tags: ['span', 'strong'],
            update_classes: ['text-muted', 'text-danger'],
        };
    },
    refresh: function(frm) {
        let idx = cint(frm.doc.has_update);
        frm.get_field('update_note').$wrapper.html(
            '<' + frm.AU.update_tags[idx]
            + 'class="' + frm.AU.update_classes[idx] + '">'
            + frm.AU.update_messages[idx]
            + '</' + frm.AU.update_tags[idx] + '>'
        );
    },
    check_for_update: function(frm) {
        if (frappe._active_users._init)
            frappe._active_users._init.request(
                'check_for_update',
                function(ret) { frm.reload_doc(); }
            );
    },
    after_save: function(frm) {
        if (frappe._active_users._init)
            frappe._active_users._init.update_settings();
    },
});