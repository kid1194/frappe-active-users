/*
*  Frappe Active Users © 2023
*  Author:  Ameen Ahmed
*  Company: Level Up Marketing & Software Development Services
*  Licence: Please refer to LICENSE file
*/


frappe.provide('frappe._active_users');
frappe.provide('frappe.dom');


class ActiveUsers {
    constructor() {
        if (frappe.desk == null) {
            frappe.throw(__('Active Users plugin can not be used outside Desk.'));
            return;
        }
        this.is_online = frappe.is_online ? frappe.is_online() : false;
        this.on_online = null;
        this.on_offline = null;
        
        var me = this;
        $(window).on('online', function() {
            me.is_online = true;
            me.on_online && me.on_online.call(me);
            me.on_online = null;
        });
        $(window).on('offline', function() {
            me.is_online = false;
            me.on_offline && me.on_offline.call(me);
            me.on_offline = null;
        });
        
        this.settings = {};
        this.data = [];
        
        this.setup();
    }
    destroy() {
        this.clear_sync();
        if (this.$loading) this.$loading.hide();
        if (this.$reload) this.$reload.off('click').hide();
        if (this.$app) this.$app.remove();
        this.data = this._on_online = this._on_offline = this._syncing = null;
        this.$app = this.$body = this.$loading = this.$footer = this.$reload = null;
    }
    error(msg, args) {
        this.destroy();
        frappe.throw(__(msg, args));
    }
    request(method, callback, type) {
        var me = this;
        return new Promise(function(resolve, reject) {
            let data = {
                method: 'active_users.utils.api.' + method,
                'async': true,
                freeze: false,
                callback: function(res) {
                    if (res && $.isPlainObject(res)) res = res.message || res;
                    if (!$.isPlainObject(res)) {
                        me.error('Active Users plugin received invalid ' + type + '.');
                        reject();
                        return;
                    }
                    if (res.error) {
                        me.error(res.message);
                        reject();
                        return;
                    }
                    let val = callback && callback.call(me, res);
                    resolve(val || res);
                }
            };
            try {
                frappe.call(data);
            } catch(e) {
                (console.error || console.log)('[Active Users]', e);
                this.error('An error has occurred while sending a request.');
                reject();
            }
        });
    }
    setup() {
        if (!this.is_online) {
            this.on_online = this.setup;
            return;
        }
        var me = this;
        this.sync_settings()
        .then(function() {
            if (!me.settings.enabled) return;
            Promise.resolve()
                .then(function() { me.setup_display(); })
                .then(function() { me.sync_reload(); });
        });
    }
    sync_settings() {
        return this.request(
            'get_settings',
            function(res) {
                res.enabled = cint(res.enabled);
                res.refresh_interval = cint(res.refresh_interval) * 60000;
                res.allow_manual_refresh = cint(res.allow_manual_refresh);
                this.settings = res;
            },
            'settings'
        );
    }
    setup_display() {
        let title = __('Active Users');
        this.$app = $(`
            <li class="nav-item dropdown dropdown-notifications dropdown-mobile active-users-navbar-item" title="${title}">
                <a class="nav-link active-users-navbar-icon text-muted"
                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="true" data-persist="true"
                    href="#" onclick="return false;">
                    <span class="fa fa-user fa-lg fa-fw"></span>
                </a>
                <div class="dropdown-menu active-users-list" role="menu">
                    <div class="fluid-container">
                        <div class="row">
                            <div class="col active-users-list-header">${title}</div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col active-users-list-body">
                            <div class="active-users-list-loading">
                                <div class="active-users-list-loading-box"></div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col active-users-list-footer">
                            <div class="row">
                                <div class="col active-users-footer-text"></div>
                                <div class="col-auto active-users-footer-icon">
                                    <a href="#" class="active-users-footer-reload">
                                        <span class="fa fa-refresh fa-md fa-fw"></span>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
        `);
        $('header.navbar > .container > .navbar-collapse > ul.navbar-nav').prepend(this.$app.get(0));
        
        this.$body = this.$app.find('.active-users-list-body');
        this.$loading = this.$body.find('.active-users-list-loading').hide();
        this.$footer = this.$app.find('.active-users-footer-text');
        this.$reload = this.$app.find('.active-users-footer-reload');
        
        this.setup_manual_sync();
    }
    setup_manual_sync() {
        if (!this.settings.allow_manual_refresh) {
            this.$reload.off('click').hide();
            return;
        }
        var me = this;
        this.$reload.on('click', function(e) {
            e.preventDefault();
            if (!me._syncing) me.sync_reload();
        }).show();
    }
    sync_reload() {
        if (!this.is_online) return;
        this.clear_sync();
        var me = this;
        Promise.resolve()
            .then(function() { me.sync_data(); })
            .then(function() { me.setup_sync(); });
    }
    clear_sync() {
        if (this.sync_timer) {
            window.clearInterval(this.sync_timer);
            this.sync_timer = null;
        }
    }
    sync_data() {
        this._syncing = true;
        if (this.data.length) {
            this.$footer.html('');
            this.$body.empty();
        }
        this.$loading.show();
        this.request(
            'get_users',
            function(res) {
                this.data = res.users && Array.isArray(res.users) ? res.users : [];
                this.$loading.hide();
                this.update_list();
                this._syncing = null;
            },
            'users list'
        );
    }
    setup_sync() {
        var me = this;
        this.sync_timer = window.setInterval(function() {
            me.sync_data();
        }, this.settings.refresh_interval);
    }
    update_settings() {
        if (!this.is_online) {
            this.on_online = this.update_settings;
            return;
        }
        var me = this;
        this.sync_settings()
        .then(function() {
            if (!me.settings.enabled) {
                me.destroy();
                return;
            }
            Promise.resolve()
                .then(function() { me.setup_manual_sync(); })
                .then(function() { me.sync_reload(); });
        });
    }
    update_list() {
        var me = this;
        this.data.forEach(function(v) {
            let avatar = frappe.get_avatar(null, v.full_name, v.user_image),
            name = v.full_name,
            item = $(`
                <div class="row active-users-list-item">
                    <div class="col-auto active-users-item-avatar">${avatar}</div>
                    <div class="col active-users-item-name">${name}</div>
                </div>
            `);
            me.$body.append(item.get(0));
        });
        this.$footer.html(__('Total') + ': ' + this.data.length);
    }
}

frappe._active_users.init = function() {
    if (frappe._active_users._init) frappe._active_users._init.destory();
    if (frappe.desk == null) return;
    frappe._active_users._init = new ActiveUsers();
};

$(document).ready(function() {
    frappe._active_users.init();
});