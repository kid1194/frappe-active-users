# Frappe Active Users
A small plugin for Frappe that displays a list of current active users.

### Table of Contents
<ul>
    <li><a href="#requirements">Requirements</a></li>
    <li>
        <a href="#setup">Setup</a>
        <ul>
            <li><a href="#install">Install</a></li>
            <li><a href="#update">Update</a></li>
            <li><a href="#uninstall">Uninstall</a></li>
        </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
</ul>

---

### Requirements
- Frappe >= v13.0.0

---

### Setup

#### Install
1. Get the plugin from Github

*(Required only once)*

`bench get-app https://github.com/kid1194/frappe-active-users`

2. Install the plugin on any instance/site you want

`bench --site [sitename] install-app active_users`

3. Check the usage section below

#### Update
1. Go to the app directory (frappe-bench/apps/active_users) and execute:

`git pull`

2. Go back to the frappe-bench directory and execute:

`bench --site [sitename] migrate`

3. *In case you need to restart bench, execute:*

`bench restart`

#### Uninstall
1. Uninstall the plugin from the instance/site

`bench --site [sitename] uninstall-app active_users`

2. Uninstall the plugin from bench

`bench remove-app active_users`

---

### Usage
1. Go to `Active Users Settings`
2. Check the `Is Enabled` box and set the desired `Refresh Interval`
3. Select the `Roles Condition` and add the `Roles` allowed to use the plugin
4. Optional, select the `Users Condition` and add the `Users` allowed to use the plugin

---

### License
MIT
