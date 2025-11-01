#!/bin/bash
# Startup script for Housing Management System on Linux XAMPP
# سكريبت بدء تشغيل نظام إدارة الإسكان على XAMPP لينكس

echo "========================================"
echo "Housing Management System - XAMPP"
echo "نظام إدارة الإسكان الجامعي"
echo "========================================"
echo ""

# Change to the script's directory
# الانتقال إلى مجلد السكريبت
cd "$(dirname "$0")"

echo "Current directory: $(pwd)"
echo "المجلد الحالي: $(pwd)"
echo ""

# Check if Python 3 is installed
# التحقق من تثبيت Python 3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "خطأ: Python 3 غير مثبت"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Load environment variables from .env file if it exists
# تحميل متغيرات البيئة من ملف .env إذا كان موجوداً
if [ -f .env ]; then
    echo "Loading environment variables from .env"
    echo "تحميل متغيرات البيئة من ملف .env"
    export $(grep -v '^#' .env | xargs)
else
    echo "WARNING: .env file not found"
    echo "تحذير: ملف .env غير موجود"
fi

# Set default environment variables if not set
# تعيين متغيرات البيئة الافتراضية إذا لم تكن معينة
export FLASK_ENV=${FLASK_ENV:-production}
export DATABASE_PATH=${DATABASE_PATH:-housing_database.db}
export HOST=${HOST:-127.0.0.1}
export PORT=${PORT:-5000}

echo ""
echo "Environment Configuration:"
echo "========================="
echo "FLASK_ENV: $FLASK_ENV"
echo "HOST: $HOST"
echo "PORT: $PORT"
echo "DATABASE_PATH: $DATABASE_PATH"
echo ""

# Check if database exists
# التحقق من وجود قاعدة البيانات
if [ ! -f "$DATABASE_PATH" ]; then
    echo "WARNING: Database file not found: $DATABASE_PATH"
    echo "تحذير: ملف قاعدة البيانات غير موجود: $DATABASE_PATH"
    echo ""
    echo "Attempting to create database..."
    echo "محاولة إنشاء قاعدة البيانات..."
    python3 generate_database.py
fi

# Check if required directories exist
# التحقق من وجود المجلدات المطلوبة
mkdir -p uploads
mkdir -p processed_images
mkdir -p logs

# Set proper permissions
# تعيين الصلاحيات المناسبة
chmod -R 755 uploads processed_images logs 2>/dev/null || true

echo ""
echo "Starting Flask application..."
echo "بدء تشغيل تطبيق Flask..."
echo ""
echo "Access the application at: http://$HOST:$PORT"
echo "يمكن الوصول للتطبيق على: http://$HOST:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo "اضغط Ctrl+C لإيقاف الخادم"
echo ""
echo "========================================"
echo ""

# Start Flask application
# بدء تطبيق Flask
python3 app.py

# Check exit status
# التحقق من حالة الخروج
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Flask application exited with error"
    echo "خطأ: تطبيق Flask توقف مع خطأ"
    echo ""
    exit 1
fi
