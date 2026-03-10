@echo off
setlocal

set "TARGET=B:\dome"

for /l %%I in (1,1,60) do (
    if not exist "%TARGET%" exit /b 0
    rmdir /s /q "%TARGET%" >nul 2>nul
    if not exist "%TARGET%" exit /b 0
    powershell.exe -NoProfile -Command "Start-Sleep -Milliseconds 1000" >nul 2>nul
)

exit /b 1
