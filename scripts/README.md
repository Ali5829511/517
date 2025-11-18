# 🚀 سكريبتات النشر السريع | Quick Deployment Scripts

دليل استخدام سكريبتات النشر التلقائي لنظام إدارة الإسكان الجامعي  
Guide for using automated deployment scripts for the University Housing Management System

---

## 📋 السكريبتات المتاحة | Available Scripts

### 1. `deploy-railway.sh` - نشر على Railway ⭐
نشر سريع على Railway.app (الموصى به)

**الاستخدام | Usage:**
```bash
./scripts/deploy-railway.sh
```

**المتطلبات | Requirements:**
- Railway CLI: `npm install -g @railway/cli`
- حساب Railway: https://railway.app

---

### 2. `deploy-flyio.sh` - نشر على Fly.io ⚡
نشر سريع على Fly.io (سريع وحديث)

**الاستخدام | Usage:**
```bash
./scripts/deploy-flyio.sh
```

**المتطلبات | Requirements:**
- Fly CLI: `curl -L https://fly.io/install.sh | sh`
- حساب Fly.io: https://fly.io

---

### 3. `deploy-heroku.sh` - نشر على Heroku 📚
نشر على Heroku (الكلاسيكي)

**الاستخدام | Usage:**
```bash
./scripts/deploy-heroku.sh
```

**المتطلبات | Requirements:**
- Heroku CLI: `brew install heroku/brew/heroku`
- حساب Heroku: https://heroku.com

---

### 4. `test-before-deploy.sh` - اختبار قبل النشر 🧪
اختبار التطبيق محلياً قبل النشر

**الاستخدام | Usage:**
```bash
./scripts/test-before-deploy.sh
```

**يقوم بـ | It does:**
- تثبيت المتطلبات
- التحقق من قاعدة البيانات
- تشغيل الاختبارات
- فحص جودة الكود
- تشغيل التطبيق للاختبار

---

## ⚡ نشر سريع في 3 خطوات | Quick Deploy in 3 Steps

### Railway (الموصى به | Recommended)

```bash
# 1. تثبيت CLI
npm install -g @railway/cli

# 2. نشر
./scripts/deploy-railway.sh

# 3. انتهى! ✅
```

### Fly.io (سريع | Fast)

```bash
# 1. تثبيت CLI
curl -L https://fly.io/install.sh | sh

# 2. نشر
./scripts/deploy-flyio.sh

# 3. انتهى! ✅
```

---

## 🔧 إعداد متغيرات البيئة | Environment Variables Setup

السكريبتات ستسألك عن إضافة `OPENAI_API_KEY` (اختياري):

```
هل تريد إضافة OPENAI_API_KEY؟ (y/n): y
أدخل OPENAI_API_KEY: sk-your-key-here
```

---

## 🐛 استكشاف الأخطاء | Troubleshooting

### المشكلة: Permission denied
```bash
chmod +x scripts/*.sh
```

### المشكلة: CLI not found
تأكد من تثبيت الـ CLI المناسب حسب المنصة

### المشكلة: Git not configured
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## 📚 المزيد من المعلومات | More Information

راجع الدليل الشامل:
- [CLOUD_DEPLOYMENT_GUIDE.md](../CLOUD_DEPLOYMENT_GUIDE.md) - دليل شامل لجميع المنصات
- [QUICK_START.md](../QUICK_START.md) - البدء السريع
- [DEVELOPMENT.md](../DEVELOPMENT.md) - دليل التطوير

---

© 2025 جامعة الإمام محمد بن سعود الإسلامية  
© 2025 Imam Muhammad bin Saud Islamic University
