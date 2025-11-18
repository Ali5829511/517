#!/bin/bash
# deploy-railway.sh - نشر سريع على Railway
# Quick Railway deployment script

echo "🚀 نشر نظام إدارة الإسكان على Railway..."
echo "🚀 Deploying Housing Management System to Railway..."

# التحقق من تثبيت Railway CLI
# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "⚠️  Railway CLI غير مثبت. قم بتثبيته أولاً:"
    echo "⚠️  Railway CLI is not installed. Install it first:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# تسجيل الدخول
# Login
echo "🔐 تسجيل الدخول... | Logging in..."
railway login

# إنشاء مشروع جديد
# Create new project
echo "📦 إنشاء مشروع جديد... | Creating new project..."
railway init

# ربط المستودع
# Link repository
railway link

# إضافة متغيرات البيئة (اختياري)
# Add environment variables (optional)
echo ""
echo "🔑 إضافة متغيرات البيئة... | Adding environment variables..."
read -p "هل تريد إضافة OPENAI_API_KEY؟ | Do you want to add OPENAI_API_KEY? (y/n): " add_key
if [ "$add_key" = "y" ]; then
    read -p "أدخل OPENAI_API_KEY | Enter OPENAI_API_KEY: " api_key
    railway variables set OPENAI_API_KEY="$api_key"
fi

# النشر
# Deploy
echo ""
echo "🚀 جاري النشر... | Deploying..."
railway up

echo ""
echo "✅ تم النشر بنجاح! | Deployment successful!"
echo "🌐 فتح التطبيق... | Opening application..."
railway open
