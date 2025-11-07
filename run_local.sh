#!/bin/bash
# تشغيل النظام محلياً
# Run System Locally

echo "=========================================="
echo "تشغيل نظام إدارة الإسكان محلياً"
echo "Running Housing Management System Locally"
echo "=========================================="
echo ""

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ خطأ: Python 3 غير مثبت"
    echo "❌ Error: Python 3 is not installed"
    echo ""
    echo "قم بتثبيت Python من: https://www.python.org/downloads/"
    echo "Install Python from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Python متوفر: $PYTHON_VERSION"
echo ""

# التحقق من وجود قاعدة البيانات
if [ ! -f "housing_database.db" ]; then
    echo "⚠️  تحذير: قاعدة البيانات غير موجودة"
    echo "⚠️  Warning: Database not found"
    echo ""
    read -p "هل تريد إنشاء قاعدة بيانات جديدة؟ (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -f "generate_database.py" ]; then
            echo "📊 إنشاء قاعدة البيانات..."
            python3 generate_database.py
        else
            echo "❌ ملف generate_database.py غير موجود"
            exit 1
        fi
    fi
fi

# التحقق من المتطلبات
echo "📦 التحقق من المتطلبات..."
echo "Checking requirements..."
echo ""

if [ ! -f "requirements.txt" ]; then
    echo "❌ خطأ: ملف requirements.txt غير موجود"
    echo "❌ Error: requirements.txt not found"
    exit 1
fi

# سؤال عن تثبيت المتطلبات
read -p "هل تريد تثبيت/تحديث المتطلبات؟ (y/n) / Install/update requirements? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 جاري تثبيت المتطلبات..."
    echo "Installing requirements..."
    pip3 install -r requirements.txt
    echo ""
fi

# إنشاء ملف .env إذا لم يكن موجوداً
if [ ! -f ".env" ]; then
    echo "⚙️  إنشاء ملف .env..."
    echo "Creating .env file..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ تم نسخ .env.example إلى .env"
        echo ""
        echo "⚠️  تنبيه: قم بتعديل ملف .env وإضافة المفاتيح المطلوبة"
        echo "⚠️  Note: Edit .env file and add required keys"
        echo "   - SECRET_KEY"
        echo "   - OPENAI_API_KEY (اختياري / optional)"
        echo ""
        read -p "اضغط Enter للمتابعة / Press Enter to continue..." 
    fi
fi

# إنشاء المجلدات المطلوبة
echo "📁 إنشاء المجلدات المطلوبة..."
echo "Creating required directories..."
mkdir -p uploads
mkdir -p processed_images
mkdir -p logs
echo "✓ المجلدات جاهزة"
echo ""

# اختيار المنفذ
DEFAULT_PORT=5000
read -p "أدخل رقم المنفذ (افتراضي: $DEFAULT_PORT) / Port number (default: $DEFAULT_PORT): " PORT
PORT=${PORT:-$DEFAULT_PORT}

echo ""
echo "=========================================="
echo "🚀 بدء تشغيل التطبيق..."
echo "🚀 Starting application..."
echo "=========================================="
echo ""
echo "📍 العنوان المحلي / Local URL:"
echo "   http://localhost:$PORT"
echo "   http://127.0.0.1:$PORT"
echo ""
echo "⚠️  للإيقاف اضغط: Ctrl+C / To stop press: Ctrl+C"
echo ""
echo "=========================================="
echo ""

# تشغيل التطبيق
export FLASK_ENV=development
export FLASK_DEBUG=1
export PORT=$PORT

python3 app.py
