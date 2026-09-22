# Employee Leave & Asset Management System

This is a beginner-friendly Django project for employee management, leave application, and asset requests.

## Features

- Authentication: register, login, logout, change password, profile page
- Employee management: view profile, edit profile, upload photo, disable employee
- Leave management: apply leave, view leave history, cancel or approve/reject leave
- Asset management: request laptop/monitor/keyboard/headset and manage approvals
- Dashboard: employee count, leave summary, pending assets
- Search and filtering: by employee name/department and leave status/date

## Traditional Django steps used

```bash
python3 -m django startproject employee_leave_asset_system .
python3 manage.py startapp hrms
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

## Run project

```bash
cd /Users/nallaamulya/Desktop/inventory management
python3 manage.py runserver
```

Open http://127.0.0.1:8000/

## Admin

Open http://127.0.0.1:8000/admin/

Login with the superuser account created by the command above.
