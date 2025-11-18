#!/bin/bash
# run_plate_system.sh - سكريبت تشغيل نظام التعرف على اللوحات
# Script to run Plate Recognition System

echo "🚗 نظام التعرف على اللوحات - Plate Recognition System"
echo "=================================================="
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت | Python 3 not installed"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"
echo ""

# التحقق من المكتبات
echo "📦 فحص المكتبات المطلوبة..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "⚠️  FastAPI غير مثبت. جاري التثبيت..."
    pip install fastapi uvicorn sqlalchemy pydantic python-dotenv pandas openpyxl jinja2 reportlab
fi

# الانتقال إلى مجلد النظام
cd plate_recognition || exit 1

# إنشاء قاعدة البيانات إذا لم تكن موجودة
if [ ! -f "plates.db" ]; then
    echo "🗄️  إنشاء قاعدة البيانات..."
fi

# تشغيل الخادم
echo ""
echo "🚀 تشغيل الخادم..."
echo "📍 الصفحة الرئيسية: http://localhost:8000"
echo "📖 التوثيق: http://localhost:8000/docs"
echo ""
echo "لإيقاف الخادم، اضغط Ctrl+C"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
