@echo off
pushd "%~dp0"
for %%a in (*.json) do (
 python generate_token_yt.py "%%~a"
)
echo удаление *.json
pause
del /f /q *.json
echo удаление token.pickle
pause
del /f /q token.pickle
pause
