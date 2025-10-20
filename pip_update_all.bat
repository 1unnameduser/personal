@echo off
pushd "%~dp0"
rem SFK is required -- https://www.stahlworks.com/

del /f /q requirements.txt
pip freeze > requirements.txt
sfk rep requirements.txt "/==/>=/" -yes
pip install -r requirements.txt --upgrade
del /f /q requirements.txt
