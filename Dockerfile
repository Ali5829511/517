# Dockerfile for University Housing Management System
# نظام إدارة الإسكان الجامعي

# استخدام Python 3.11 slim للحجم الأصغر
# Use Python 3.11 slim for smaller size
FROM python:3.11-slim

# تعيين متغيرات البيئة
# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8080

# تعيين مجلد العمل
# Set working directory
WORKDIR /app

# تثبيت dependencies النظام المطلوبة
# Install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات أولاً للاستفادة من Docker cache
# Copy requirements first for better Docker cache usage
COPY requirements.txt .

# تثبيت متطلبات Python
# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات التطبيق
# Copy all application files
COPY . .

# إنشاء المجلدات المطلوبة
# Create required directories
RUN mkdir -p uploads processed_images logs

# إعطاء أذونات التنفيذ للسكريبتات
# Give execution permissions to scripts
RUN chmod +x *.sh 2>/dev/null || true

# تعريف المنفذ
# Expose port
EXPOSE 8080

# الأمر الافتراضي لتشغيل التطبيق
# Default command to run the application
CMD exec gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --threads 8 \
    --timeout 120 \
    --worker-class sync \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile -
