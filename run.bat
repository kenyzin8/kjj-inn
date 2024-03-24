@ECHO OFF
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& { . '..\env\Scripts\Activate.ps1'; python manage.py runserver }"
