#!/bin/bash
# deploy-flyio.sh - نشر سريع على Fly.io
# Quick Fly.io deployment script

echo "⚡ نشر نظام إدارة الإسكان على Fly.io..."
echo "⚡ Deploying Housing Management System to Fly.io..."

# التحقق من تثبيت Fly CLI
# Check if Fly CLI is installed
if ! command -v fly &> /dev/null; then
    echo "⚠️  Fly CLI غير مثبت. قم بتثبيته أولاً:"
    echo "⚠️  Fly CLI is not installed. Install it first:"
    echo "curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# تسجيل الدخول
# Login
echo "🔐 تسجيل الدخول... | Logging in..."
fly auth login

# إنشاء التطبيق
# Create application
echo "📦 إنشاء التطبيق... | Creating application..."
fly launch --name housing-system --region iad --no-deploy

# إضافة متغيرات البيئة (اختياري)
# Add environment variables (optional)
echo ""
echo "🔑 إضافة متغيرات البيئة... | Adding environment variables..."
read -p "هل تريد إضافة OPENAI_API_KEY؟ | Do you want to add OPENAI_API_KEY? (y/n): " add_key
if [ "$add_key" = "y" ]; then
    read -p "أدخل OPENAI_API_KEY | Enter OPENAI_API_KEY: " api_key
    fly secrets set OPENAI_API_KEY="$api_key"
fi

# النشر
# Deploy
echo ""
echo "🚀 جاري النشر... | Deploying..."
fly deploy

echo ""
echo "✅ تم النشر بنجاح! | Deployment successful!"
echo "🌐 فتح التطبيق... | Opening application..."
fly open
