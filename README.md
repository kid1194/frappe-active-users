# Frappe Active Users

A small plugin for Frappe that displays a list of current active users.

<p align="center">
    <img src="https://github.com/kid1194/frappe-active-users/blob/main/images/image.png?raw=true" alt="Active Users"/>
</p>

---

### Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
  - [Install](#install)
  - [Update](#update)
  - [Uninstall](#uninstall)
- [Usage](#usage)
- [Contributors](#contributors)
- [Issues](#issues)
- [License](#license)

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
bench build --app active_users
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
bench build --app active_users
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
3. Choose the **Roles** and **Users** that you want the plugin to be visible to or hidden from

---

### Contributors
- [Monolith Online](https://github.com/monolithon) (Testing & Debugging)

---

### Issues
If you find bug in the plugin, please create a [bug report](https://github.com/kid1194/frappe-active-users/issues/new?assignees=kid1194&labels=bug&template=bug_report.md&title=%5BBUG%5D) and let us know about it.

---

### License
This repository has been released under the [MIT License](https://github.com/kid1194/frappe-active-users/blob/main/LICENSE).
