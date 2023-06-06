@echo off
start cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8000"
