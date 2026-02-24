@echo off

title NVIDIA Broadcast Block Update

for %%a in (in out) do (
    echo %%a
    netsh advfirewall firewall add rule name="@___NVIDIA Broadcast Block Update" dir=%%a action=block profile=any program="%%ProgramFiles%%\NVIDIA Corporation\NVIDIA Broadcast\NVIDIA Broadcast UI.exe"
)
pause
