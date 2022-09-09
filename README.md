# Frappe Active Users

A small plugin for Frappe that displays a list of current active users.

---

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

⚠️ *Important* ⚠️

*Do not forget to replace [sitename] with the name of your site in all commands.*

#### Install
1. Go to bench directory

```
cd ~/frappe-bench
```

2. Get plugin from Github

*(Required only once)*

```
bench get-app https://github.com/kid1194/frappe-active-users
```

3. Build plugin

*(Required only once)*

```
bench build --apps active_users
```

4. Install plugin on a specific site

```
bench --site [sitename] install-app active_users
```

5. Check the usage section below

#### Update
1. Go to app directory

```
cd ~/frappe-bench/apps/active_users
```

2. Get updates from Github

```
git pull
```

3. Go to bench directory

```
cd ~/frappe-bench
```

4. Build plugin

```
bench build --apps active_users
```

5. Update a specific site

```
bench --site [sitename] migrate
```

6. Restart bench

```
bench restart
```

#### Uninstall
1. Go to bench directory

```
cd ~/frappe-bench
```

2. Uninstall plugin from a specific site

```
bench --site [sitename] uninstall-app active_users
```

3. Remove plugin from bench

```
bench remove-app active_users
```

4. Restart bench

```
bench restart
```

---

### Usage
1. Go to **Active Users Settings**
2. Check the **Is Enabled** box and set the desired **Refresh Interval**
3. Select the **Roles Condition** and add the **Roles** allowed to use the plugin
4. **Optional**, select the **Users Condition** and add the **Users** allowed to use the plugin

---

### License
MIT
