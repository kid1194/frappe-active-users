/*
*  Frappe Active Users © 2022
*  Author:  Ameen Ahmed
*  Company: Level Up Marketing & Software Development Services
*  Licence: Please refer to license.txt
*/

frappe.provide('frappe.ActiveUsers');
frappe.provide('frappe._active_users');

frappe.ActiveUsers = class ActiveUsers {
    constructor() {
        if (frappe.desk == null) {
            frappe.throw(_('Active Users plugin can not be used outside Desk.'))
            return;
        }
        this.settings = {};
        this.data = [];
        this.setup_app();
    }
    setup_app() {
        var me = this;
        this.sync_settings()
        .then(function() {
            if (!me.settings.is_enabled) return;
            frappe.run_serially([
                me.setup_display,
                me.sync_data,
            ]);
        });
    }
    update_settings() {
        var me = this;
        this.sync_settings()
        .then(function() {
            if (!me.settings.is_enabled) me.destroy();
        });
    }
    sync_settings() {
        var me = this,
        promise = frappe.call({
            type: 'GET',
            method: 'active_users.api.handler.get_settings',
        });
        promise.then(function(res) {
            me.settings = res.message;
        });
        return promise;
    }
    setup_display() {
        $('header.navbar > .container > .navbar-collapse > ul').prepend(`
            <li
                class="nav-item dropdown dropdown-notifications dropdown-mobile hidden active-users-navbar-icon"
                title="{{ _('Active Users') }}">
                <a class="nav-link active-users-icon text-muted"
                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"
                    href="#" onclick="return false;">
                    <span class="fa fa-users fa-md fa-fw"></span>
                </a>
                <div class="dropdown-menu active-users-list dropdown-menu-right" role="menu">
                    <div class="active-users-list-header">
                        {{ _('Active Users') }}
                    </div>
                    <div class="active-users-list-body"></div>
                    <div class="active-users-list-footer"></div>
                </div>
            </li>
        `);
        
        this.$app = $('.active-users-navbar-icon');
        this.$body = $('.active-users-list-body');
        this.$footer = $('.active-users-list-footer');
    }
    setup_sync() {
        var me = this,
        delay = cint(this.settings.refresh_interval) * 60000;
        frappe.timeout(delay).then(function() { me.sync_data(); });
    }
    sync_data() {
        var me = this;
        frappe.call({
            type: 'GET',
            method: 'active_users.api.handler.get_users',
        }).then(function(res) {
            me.data = res.message;
            frappe.run_serially([
                me.update_list,
                me.setup_sync,
            ]);
        });
    }
    update_list() {
        this.$body.empty();
        var me = this;
        this.data.forEach(function(v) {
            let avatar = frappe.get_avatar(null, v.full_name, v.user_image),
            name = v.full_name;
            me.$body.append(`
                <div class="active-users-list-item">
                    <div class="active-users-item-avatar">${avatar}</div>
                    <div class="active-users-item-name">${name}</div>
                </div>
            `);
        });
        this.$footer.html(_('Total') + ': ' + this.data.length);
    }
    destory() {
        this.$app.remove();
        this.data = this.$app = this.$body = this.$footer = null;
    }
};

frappe.ActiveUsers.start = function() {
    if (frappe._active_users) frappe._active_users.destory();
    if (frappe.desk == null) return;
    frappe._active_users = new frappe.ActiveUsers();
};
        
$(document).ready(function() { frappe.ActiveUsers.start(); });