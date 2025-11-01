@echo off
REM Startup script for Housing Management System on Windows XAMPP
REM سكريبت بدء تشغيل نظام إدارة الإسكان على XAMPP ويندوز

echo ========================================
echo Housing Management System - XAMPP
echo نظام إدارة الإسكان الجامعي
echo ========================================
echo.

REM Change to the project directory
REM الانتقال إلى مجلد المشروع
cd /d "%~dp0"

echo Current directory: %CD%
echo المجلد الحالي: %CD%
echo.

REM Check if Python is installed
REM التحقق من تثبيت Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo خطأ: Python غير مثبت أو غير موجود في PATH
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Load environment variables from .env file if it exists
REM تحميل متغيرات البيئة من ملف .env إذا كان موجوداً
if exist .env (
    echo Loading environment variables from .env
    echo تحميل متغيرات البيئة من ملف .env
    for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
        if not "%%a"=="" if not "%%a"=="#" (
            set "%%a=%%b"
        )
    )
) else (
    echo WARNING: .env file not found
    echo تحذير: ملف .env غير موجود
)

REM Set default environment variables if not set
REM تعيين متغيرات البيئة الافتراضية إذا لم تكن معينة
if not defined FLASK_ENV set FLASK_ENV=production
if not defined DATABASE_PATH set DATABASE_PATH=housing_database.db
if not defined HOST set HOST=127.0.0.1
if not defined PORT set PORT=5000

echo.
echo Environment Configuration:
echo =========================
echo FLASK_ENV: %FLASK_ENV%
echo HOST: %HOST%
echo PORT: %PORT%
echo DATABASE_PATH: %DATABASE_PATH%
echo.

REM Check if database exists
REM التحقق من وجود قاعدة البيانات
if not exist "%DATABASE_PATH%" (
    echo WARNING: Database file not found: %DATABASE_PATH%
    echo تحذير: ملف قاعدة البيانات غير موجود: %DATABASE_PATH%
    echo.
    echo Attempting to create database...
    echo محاولة إنشاء قاعدة البيانات...
    python generate_database.py
)

REM Check if required directories exist
REM التحقق من وجود المجلدات المطلوبة
if not exist "uploads" mkdir uploads
if not exist "processed_images" mkdir processed_images
if not exist "logs" mkdir logs

echo.
echo Starting Flask application...
echo بدء تشغيل تطبيق Flask...
echo.
echo Access the application at: http://%HOST%:%PORT%
echo يمكن الوصول للتطبيق على: http://%HOST%:%PORT%
echo.
echo Press Ctrl+C to stop the server
echo اضغط Ctrl+C لإيقاف الخادم
echo.
echo ========================================
echo.

REM Start Flask application
REM بدء تطبيق Flask
python app.py

REM If Flask exits, pause to see any error messages
REM إذا توقف Flask، توقف لرؤية رسائل الخطأ
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Flask application exited with error code: %errorlevel%
    echo خطأ: تطبيق Flask توقف مع رمز خطأ: %errorlevel%
    echo.
    pause
)
