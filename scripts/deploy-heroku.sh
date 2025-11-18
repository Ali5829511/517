#!/bin/bash
# deploy-heroku.sh - نشر سريع على Heroku
# Quick Heroku deployment script

echo "📚 نشر نظام إدارة الإسكان على Heroku..."
echo "📚 Deploying Housing Management System to Heroku..."

# التحقق من تثبيت Heroku CLI
# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "⚠️  Heroku CLI غير مثبت. قم بتثبيته أولاً"
    echo "⚠️  Heroku CLI is not installed. Install it first"
    echo "Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# تسجيل الدخول
# Login
echo "🔐 تسجيل الدخول... | Logging in..."
heroku login

# إنشاء التطبيق
# Create application
echo ""
echo "📦 إنشاء التطبيق... | Creating application..."
read -p "أدخل اسم التطبيق (أو اضغط Enter لاسم عشوائي) | Enter app name (or press Enter for random): " app_name
if [ -z "$app_name" ]; then
    heroku create
else
    heroku create "$app_name"
fi

# إضافة متغيرات البيئة
# Add environment variables
echo ""
echo "🔑 إضافة متغيرات البيئة... | Adding environment variables..."
heroku config:set FLASK_ENV=production

read -p "هل تريد إضافة OPENAI_API_KEY؟ | Do you want to add OPENAI_API_KEY? (y/n): " add_key
if [ "$add_key" = "y" ]; then
    read -p "أدخل OPENAI_API_KEY | Enter OPENAI_API_KEY: " api_key
    heroku config:set OPENAI_API_KEY="$api_key"
fi

# النشر
# Deploy
echo ""
echo "🚀 جاري النشر... | Deploying..."
git push heroku main

# فتح التطبيق
# Open application
echo ""
echo "✅ تم النشر بنجاح! | Deployment successful!"
echo "🌐 فتح التطبيق... | Opening application..."
heroku open
