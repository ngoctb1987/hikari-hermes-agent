@echo off
title Hermes Gateway (Telegram)
echo ==================================================
echo Dang khoi dong Hermes Gateway...
echo ==================================================
d:
cd d:\hikari-hermes-agent
set PYTHONIOENCODING=utf-8
call venv\Scripts\activate.bat
hermes gateway
echo ==================================================
echo Hermes Gateway da dung.
echo ==================================================
pause
