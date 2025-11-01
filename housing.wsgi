#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
WSGI File for Housing Management System
ملف WSGI لنظام إدارة الإسكان الجامعي

This file is used to deploy the Flask application with mod_wsgi in Apache.
هذا الملف يُستخدم لنشر تطبيق Flask باستخدام mod_wsgi في Apache.

Usage in Apache configuration:
استخدام في تكوين Apache:

WSGIScriptAlias /housing /path/to/housing-system/housing.wsgi

<Directory /path/to/housing-system>
    WSGIProcessGroup housing
    WSGIApplicationGroup %{GLOBAL}
    Require all granted
</Directory>
"""

import sys
import os
import logging

# Setup logging for WSGI
# إعداد تسجيل الأخطاء لـ WSGI
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# Get the directory containing this file
# الحصول على المجلد الذي يحتوي هذا الملف
project_home = os.path.dirname(os.path.abspath(__file__))

# Add project directory to Python path
# إضافة مجلد المشروع إلى مسار Python
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
# تعيين متغيرات البيئة
# NOTE: In production, use environment variables or a separate config file
# ملاحظة: في الإنتاج، استخدم متغيرات البيئة أو ملف تكوين منفصل

# Load from .env file if it exists
# تحميل من ملف .env إذا كان موجوداً
env_file = os.path.join(project_home, '.env')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Set default values if not in environment
# تعيين القيم الافتراضية إذا لم تكن في البيئة
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('DATABASE_PATH', os.path.join(project_home, 'housing_database.db'))
os.environ.setdefault('UPLOAD_FOLDER', os.path.join(project_home, 'uploads'))
os.environ.setdefault('PROCESSED_FOLDER', os.path.join(project_home, 'processed_images'))

# Create necessary directories
# إنشاء المجلدات الضرورية
upload_folder = os.environ.get('UPLOAD_FOLDER')
processed_folder = os.environ.get('PROCESSED_FOLDER')

if upload_folder and not os.path.exists(upload_folder):
    os.makedirs(upload_folder, exist_ok=True)

if processed_folder and not os.path.exists(processed_folder):
    os.makedirs(processed_folder, exist_ok=True)

# Import the Flask application
# استيراد تطبيق Flask
try:
    from app import app as application
    logging.info("Flask application loaded successfully")
except Exception as e:
    logging.error(f"Failed to load Flask application: {e}")
    raise

# Optional: Set application configuration
# اختياري: تعيين تكوين التطبيق
application.config['DEBUG'] = False

# Log successful initialization
# تسجيل التهيئة الناجحة
logging.info(f"WSGI application initialized from: {project_home}")
logging.info(f"Database path: {os.environ.get('DATABASE_PATH')}")
logging.info(f"Upload folder: {os.environ.get('UPLOAD_FOLDER')}")
