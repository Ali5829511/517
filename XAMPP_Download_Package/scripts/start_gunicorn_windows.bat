@echo off
REM Startup script for Housing Management System with Gunicorn on Windows
REM سكريبت بدء تشغيل نظام إدارة الإسكان باستخدام Gunicorn على ويندوز

echo ========================================
echo Housing Management System - Gunicorn
echo نظام إدارة الإسكان الجامعي - Gunicorn
echo ========================================
echo.

REM Change to the project directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Load environment variables from .env file if it exists
if exist .env (
    echo Loading environment variables from .env
    for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
        if not "%%a"=="" if not "%%a"=="#" (
            set "%%a=%%b"
        )
    )
)

REM Set default values
if not defined FLASK_ENV set FLASK_ENV=production
if not defined HOST set HOST=127.0.0.1
if not defined PORT set PORT=5000
if not defined WORKERS set WORKERS=4

echo Environment Configuration:
echo =========================
echo FLASK_ENV: %FLASK_ENV%
echo HOST: %HOST%
echo PORT: %PORT%
echo WORKERS: %WORKERS%
echo.

REM Create required directories
if not exist "uploads" mkdir uploads
if not exist "processed_images" mkdir processed_images
if not exist "logs" mkdir logs

echo Starting Gunicorn server...
echo بدء تشغيل خادم Gunicorn...
echo.
echo Access the application at: http://%HOST%:%PORT%
echo.
echo Press Ctrl+C to stop the server
echo اضغط Ctrl+C لإيقاف الخادم
echo.
echo ========================================
echo.

REM Start Gunicorn with specified configuration
gunicorn ^
    --workers %WORKERS% ^
    --bind %HOST%:%PORT% ^
    --timeout 120 ^
    --access-logfile logs/gunicorn-access.log ^
    --error-logfile logs/gunicorn-error.log ^
    --log-level info ^
    app:app

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Gunicorn exited with error code: %errorlevel%
    echo.
    pause
)
