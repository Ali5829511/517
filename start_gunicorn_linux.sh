#!/bin/bash
# Startup script for Housing Management System with Gunicorn on Linux
# سكريبت بدء تشغيل نظام إدارة الإسكان باستخدام Gunicorn على لينكس

echo "========================================"
echo "Housing Management System - Gunicorn"
echo "نظام إدارة الإسكان الجامعي - Gunicorn"
echo "========================================"
echo ""

# Change to the script's directory
cd "$(dirname "$0")"

echo "Current directory: $(pwd)"
echo ""

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env"
    export $(grep -v '^#' .env | xargs)
fi

# Set default values
export FLASK_ENV=${FLASK_ENV:-production}
export HOST=${HOST:-127.0.0.1}
export PORT=${PORT:-5000}
export WORKERS=${WORKERS:-4}

echo "Environment Configuration:"
echo "========================="
echo "FLASK_ENV: $FLASK_ENV"
echo "HOST: $HOST"
echo "PORT: $PORT"
echo "WORKERS: $WORKERS"
echo ""

# Create required directories
mkdir -p uploads processed_images logs
chmod -R 755 uploads processed_images logs 2>/dev/null || true

echo "Starting Gunicorn server..."
echo "بدء تشغيل خادم Gunicorn..."
echo ""
echo "Access the application at: http://$HOST:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo "اضغط Ctrl+C لإيقاف الخادم"
echo ""
echo "========================================"
echo ""

# Start Gunicorn with specified configuration
gunicorn \
    --workers $WORKERS \
    --bind $HOST:$PORT \
    --timeout 120 \
    --access-logfile logs/gunicorn-access.log \
    --error-logfile logs/gunicorn-error.log \
    --log-level info \
    app:app

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Gunicorn exited with error"
    echo ""
    exit 1
fi
