@echo off
REM تشغيل النظام محلياً
REM Run System Locally

chcp 65001 >nul
echo ==========================================
echo تشغيل نظام إدارة الإسكان محلياً
echo Running Housing Management System Locally
echo ==========================================
echo.

REM التحقق من وجود Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت
    echo ❌ Error: Python is not installed
    echo.
    echo قم بتثبيت Python من: https://www.python.org/downloads/
    echo Install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python متوفر: %PYTHON_VERSION%
echo.

REM التحقق من وجود قاعدة البيانات
if not exist "housing_database.db" (
    echo ⚠️  تحذير: قاعدة البيانات غير موجودة
    echo ⚠️  Warning: Database not found
    echo.
    set /p CREATE_DB=هل تريد إنشاء قاعدة بيانات جديدة؟ (y/n^): 
    if /i "!CREATE_DB!"=="y" (
        if exist "generate_database.py" (
            echo 📊 إنشاء قاعدة البيانات...
            python generate_database.py
        ) else (
            echo ❌ ملف generate_database.py غير موجود
            pause
            exit /b 1
        )
    )
)

REM التحقق من المتطلبات
echo 📦 التحقق من المتطلبات...
echo Checking requirements...
echo.

if not exist "requirements.txt" (
    echo ❌ خطأ: ملف requirements.txt غير موجود
    echo ❌ Error: requirements.txt not found
    pause
    exit /b 1
)

REM سؤال عن تثبيت المتطلبات
set /p INSTALL_REQ=هل تريد تثبيت/تحديث المتطلبات؟ (y/n^): 
if /i "%INSTALL_REQ%"=="y" (
    echo 📥 جاري تثبيت المتطلبات...
    echo Installing requirements...
    pip install -r requirements.txt
    echo.
)

REM إنشاء ملف .env إذا لم يكن موجوداً
if not exist ".env" (
    echo ⚙️  إنشاء ملف .env...
    echo Creating .env file...
    
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ✓ تم نسخ .env.example إلى .env
        echo.
        echo ⚠️  تنبيه: قم بتعديل ملف .env وإضافة المفاتيح المطلوبة
        echo ⚠️  Note: Edit .env file and add required keys
        echo    - SECRET_KEY
        echo    - OPENAI_API_KEY (اختياري / optional^)
        echo.
        pause
    )
)

REM إنشاء المجلدات المطلوبة
echo 📁 إنشاء المجلدات المطلوبة...
echo Creating required directories...
if not exist "uploads" mkdir uploads
if not exist "processed_images" mkdir processed_images
if not exist "logs" mkdir logs
echo ✓ المجلدات جاهزة
echo.

REM اختيار المنفذ
set DEFAULT_PORT=5000
set /p PORT=أدخل رقم المنفذ (افتراضي: %DEFAULT_PORT%^): 
if "%PORT%"=="" set PORT=%DEFAULT_PORT%

echo.
echo ==========================================
echo 🚀 بدء تشغيل التطبيق...
echo 🚀 Starting application...
echo ==========================================
echo.
echo 📍 العنوان المحلي / Local URL:
echo    http://localhost:%PORT%
echo    http://127.0.0.1:%PORT%
echo.
echo ⚠️  للإيقاف اضغط: Ctrl+C / To stop press: Ctrl+C
echo.
echo ==========================================
echo.

REM تشغيل التطبيق
set FLASK_ENV=development
set FLASK_DEBUG=1
set PORT=%PORT%

python app.py
