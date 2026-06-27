@echo off
title Hermes Agent
echo ==================================================
echo Dang khoi dong Hermes Agent...
echo ==================================================
d:
cd d:\hikari-hermes-agent
call venv\Scripts\activate.bat
hermes
echo ==================================================
echo Hermes Agent da dung.
echo ==================================================
pause
