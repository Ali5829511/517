#!/bin/bash
# test-before-deploy.sh - اختبار قبل النشر
# Test before deployment script

echo "🧪 اختبار نظام إدارة الإسكان قبل النشر..."
echo "🧪 Testing Housing Management System before deployment..."

# تفعيل البيئة الافتراضية إذا كانت موجودة
# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "📦 تفعيل البيئة الافتراضية... | Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "📦 تفعيل البيئة الافتراضية... | Activating virtual environment..."
    source .venv/bin/activate
fi

# تثبيت المتطلبات
# Install requirements
echo "📦 تثبيت المتطلبات... | Installing requirements..."
pip install -r requirements.txt

# التحقق من قاعدة البيانات
# Check database
echo ""
echo "💾 التحقق من قاعدة البيانات... | Checking database..."
if [ ! -f "housing_database.db" ]; then
    echo "⚠️  قاعدة البيانات غير موجودة، جاري إنشائها..."
    echo "⚠️  Database not found, creating..."
    python generate_database.py
fi

# إنشاء المجلدات المطلوبة
# Create required directories
echo ""
echo "📁 إنشاء المجلدات المطلوبة... | Creating required directories..."
mkdir -p uploads processed_images logs

# تشغيل الاختبارات
# Run tests
echo ""
echo "🧪 تشغيل الاختبارات... | Running tests..."
if [ -f "test_app.py" ]; then
    python -m pytest test_app.py -v || echo "⚠️ بعض الاختبارات فشلت | Some tests failed"
else
    echo "⚠️ لا توجد اختبارات | No tests found"
fi

# فحص الكود
# Check code quality
echo ""
echo "🔍 فحص جودة الكود... | Checking code quality..."
if command -v flake8 &> /dev/null; then
    flake8 app.py --max-line-length=100 --ignore=E501,W503 || echo "⚠️ بعض مشاكل الجودة | Some quality issues found"
else
    echo "⚠️ flake8 غير مثبت | flake8 not installed"
fi

# تشغيل التطبيق للاختبار
# Run application for testing
echo ""
echo "✅ الاختبارات اكتملت! | Tests completed!"
echo ""
echo "🚀 تشغيل التطبيق للاختبار... | Running application for testing..."
echo "التطبيق يعمل على | Application running on: http://localhost:5000"
echo "اضغط Ctrl+C للإيقاف | Press Ctrl+C to stop"
echo ""
python app.py
