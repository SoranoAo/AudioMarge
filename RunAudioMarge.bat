@echo off
REM env variable setting
setlocal

REM check Python path
where python
if %errorlevel% neq 0 (
    echo "Error. Python path not found"
    pause
    exit /b %errorlevel%
)


call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo "Error. Failed active venv"
    pause
    exit /b %errorlevel%
)



python AudioMarge.py
if %errorlevel% neq 0 (
    echo "Error. Failed Run AudioMarge"
    pause
    exit /b %errorlevel%
)


