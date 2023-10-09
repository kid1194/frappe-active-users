/*
*  Active Users © 2023
*  Author:  Ameen Ahmed
*  Company: Level Up Marketing & Software Development Services
*  Licence: Please refer to LICENSE file
*/

frappe.provide('frappe._active_users');

frappe.ui.form.on('Active Users Settings', {
    setup: function(frm) {
        frm._visibility_ready = false;
        frm._update = {
            ready: false,
            messages: [
                __('App is up to date'),
                __('A new version is available'),
            ],
            tags: ['span', 'strong'],
            classes: ['text-muted', 'text-danger'],
        };
    },
    refresh: function(frm) {
        if (!frm._visibility_ready) {
            frm._visibility_ready = true;
            frm.get_field('visibility_note').$wrapper.html(
                '<div class="font-weight-bold mb-1">' + __('Note') + ':</div>'
                + '<ul>'
                    + '<li>'
                        + __(
                            'If the user has any of the listed {0}, '
                            + 'then the visibility of the plugin will depend on the '
                            + 'status of the {1} checkbox.',
                            [
                                '<code>' + __('Roles') + '</code>',
                                '<code>' + __('Hidden From Listed Roles') + '</code>'
                            ]
                        )
                    + '</li>'
                    + '<li class="mt-1">'
                        + __(
                            'If the user exists in the listed {0}, '
                            + 'then the visibility of the plugin will '
                            + 'depend on the status of the {1} checkbox, '
                            + 'bypassing the visibility status of listed {2}.',
                            [
                                '<code>' + __('Users') + '</code>',
                                '<code>' + __('Hidden From Listed Users') + '</code>',
                                '<code>' + __('Roles') + '</code>'
                            ]
                        )
                    + '</li>'
                + '</ul>'
            );
        }
        if (!frm._update.ready) {
            frm._update.ready = true;
            let idx = cint(frm.doc.has_update);
            frm.get_field('update_note').$wrapper.html(
                '<' + frm._update.tags[idx]
                + 'class="' + frm._update.classes[idx] + '">'
                + frm._update.messages[idx]
                + '</' + frm._update.tags[idx] + '>'
            );
        }
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