# دليل النشر السحابي
# Cloud Deployment Guide

## نظرة عامة | Overview

هذا الدليل يوضح كيفية نشر نظام إدارة الإسكان على منصات سحابية مختلفة.

This guide explains how to deploy the Housing Management System to various cloud platforms.

---

## ⚡ النشر السريع | Quick Deploy

### 1️⃣ Railway (موصى به | Recommended)

**الأسهل والأسرع | Easiest and Fastest**

```bash
# 1. سجل دخول على Railway
https://railway.app

# 2. اضغط "New Project"
# 3. اختر "Deploy from GitHub repo"
# 4. اختر المستودع: Ali5829511/517
# 5. اختر الفرع: main (بعد الدمج)

# 6. أضف متغيرات البيئة:
PLATE_RECOGNIZER_TOKEN=your-token-here
TAKAMUL_API_URL=https://your-takamul-url
TAKAMUL_API_KEY=your-takamul-key
```

**النتيجة:**
- ✅ رابط تلقائي: `https://your-app.up.railway.app`
- ✅ SSL تلقائي (HTTPS)
- ✅ نشر تلقائي عند كل commit
- ✅ قاعدة البيانات مدمجة

**التكلفة:** $5/شهر للمشاريع الصغيرة

---

### 2️⃣ Render.com

**بديل مجاني رائع | Great Free Alternative**

```bash
# 1. سجل دخول على Render
https://render.com

# 2. اضغط "New +" → "Web Service"
# 3. اربط GitHub repo
# 4. الإعدادات:
#    - Name: housing-system
#    - Environment: Python 3
#    - Build Command: pip install -r requirements.txt
#    - Start Command: gunicorn app:app
```

**متغيرات البيئة في Render:**
```env
PLATE_RECOGNIZER_TOKEN=your-token
TAKAMUL_API_URL=your-url
TAKAMUL_API_KEY=your-key
FLASK_ENV=production
```

**النتيجة:**
- ✅ رابط مجاني: `https://housing-system.onrender.com`
- ✅ SSL تلقائي
- ✅ نشر تلقائي
- ⚠️ قد يتوقف بعد 15 دقيقة من عدم الاستخدام (خطة مجانية)

**التكلفة:** مجاني (مع قيود) أو $7/شهر

---

### 3️⃣ Heroku

**الأكثر شهرة | Most Popular**

```bash
# 1. ثبت Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. سجل دخول
heroku login

# 3. أنشئ تطبيق
heroku create housing-system-517

# 4. أضف متغيرات البيئة
heroku config:set PLATE_RECOGNIZER_TOKEN=your-token
heroku config:set TAKAMUL_API_URL=your-url
heroku config:set TAKAMUL_API_KEY=your-key

# 5. انشر
git push heroku main
```

**التكلفة:** $7/شهر (لا توجد خطة مجانية بعد الآن)

---

### 4️⃣ Vercel (للتطبيقات الخفيفة)

```bash
# 1. ثبت Vercel CLI
npm install -g vercel

# 2. سجل دخول
vercel login

# 3. انشر
vercel --prod
```

**ملاحظة:** Vercel مناسب للتطبيقات الخفيفة فقط.

---

### 5️⃣ PythonAnywhere

**مناسب للمبتدئين | Beginner Friendly**

```bash
# 1. سجل على PythonAnywhere
https://www.pythonanywhere.com

# 2. افتح Bash Console
# 3. استنسخ المستودع
git clone https://github.com/Ali5829511/517.git
cd 517

# 4. ثبت المكتبات
pip install -r requirements.txt

# 5. طبق قاعدة البيانات
python apply_migrations.py

# 6. في Web tab:
#    - Source code: /home/yourusername/517
#    - Working directory: /home/yourusername/517
#    - WSGI file: تعديل ليشير إلى app:app
```

**التكلفة:** مجاني (مع قيود) أو من $5/شهر

---

## 📋 خطوات ما بعد النشر | Post-Deployment Steps

### 1. تطبيق قاعدة البيانات

بعد النشر الأول، قم بتطبيق التغييرات على قاعدة البيانات:

```bash
# على Railway/Render/Heroku
# افتح Shell/Console وشغل:
python apply_migrations.py
```

### 2. اختبار النظام

```bash
# اختبر API endpoints
curl https://your-domain.com/api/vehicles/statistics
curl https://your-domain.com/api/violations/statistics
```

### 3. إعداد Webhook

سجل webhook على Plate Recognizer:
```
URL: https://your-domain.com/api/webhooks/plate-recognizer
Method: POST
```

---

## 🔐 الأمان | Security

### متغيرات البيئة الإلزامية:

```env
# Plate Recognizer
PLATE_RECOGNIZER_TOKEN=sk-xxxxx

# Takamul Integration
TAKAMUL_API_URL=https://api.takamul.com
TAKAMUL_API_KEY=xxxxx

# Flask
SECRET_KEY=generate-strong-secret-key
FLASK_ENV=production

# Database (إذا كانت خارجية)
DATABASE_PATH=/app/housing_database.db
```

### توليد SECRET_KEY قوي:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🚀 النشر التلقائي | Auto-Deploy

### Railway / Render / Heroku

النشر التلقائي مفعّل افتراضياً. عند push إلى main:
```bash
git push origin main
# ✅ سيتم النشر تلقائياً
```

### إيقاف النشر التلقائي:

**Railway:**
- Settings → Deployments → Auto Deploy → Off

**Render:**
- Settings → Auto-Deploy → Disable

---

## 🔍 استكشاف الأخطاء | Troubleshooting

### المشكلة: التطبيق لا يعمل

```bash
# 1. تحقق من السجلات
# Railway:
railway logs

# Render:
# Dashboard → Logs

# Heroku:
heroku logs --tail

# 2. تحقق من المتغيرات
heroku config  # أو من Dashboard
```

### المشكلة: قاعدة البيانات فارغة

```bash
# طبق migrations
python apply_migrations.py

# تحقق من الجداول
python -c "import sqlite3; conn = sqlite3.connect('housing_database.db'); print(conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall())"
```

### المشكلة: Webhook لا يعمل

```bash
# 1. تحقق من URL صحيح
curl -X POST https://your-domain.com/api/webhooks/plate-recognizer \
  -H "Content-Type: application/json" \
  -d '{"results": [{"plate": "TEST123"}]}'

# 2. تحقق من السجل
curl https://your-domain.com/api/plate-recognizer/logs
```

---

## 📊 المقارنة | Comparison

| المنصة | السعر | النشر التلقائي | SSL | قاعدة البيانات | الأداء |
|--------|------|----------------|-----|----------------|---------|
| **Railway** | $5/شهر | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Render** | مجاني/$7 | ✅ | ✅ | ⚠️ | ⭐⭐⭐⭐ |
| **Heroku** | $7/شهر | ✅ | ✅ | إضافي | ⭐⭐⭐⭐⭐ |
| **Vercel** | مجاني | ✅ | ✅ | ❌ | ⭐⭐⭐ |
| **PythonAnywhere** | مجاني/$5 | ❌ | ✅ | ✅ | ⭐⭐⭐ |

---

## 🎯 التوصية | Recommendation

### للإنتاج:
**Railway** - أفضل توازن بين السعر والأداء والسهولة

### للتطوير والاختبار:
**Render** (الخطة المجانية) - مثالي للبداية

### للمشاريع الكبيرة:
**Heroku** أو **AWS** - أداء عالي وموثوقية

---

## 📝 ملاحظات مهمة | Important Notes

1. **قاعدة البيانات:** 
   - الملف `housing_database.db` مضمن في المستودع
   - للإنتاج، فكر في استخدام PostgreSQL أو MySQL

2. **الصور:**
   - مجلد `uploads/` للصور المؤقتة
   - للإنتاج، استخدم S3 أو خدمة تخزين سحابية

3. **الأداء:**
   - استخدم gunicorn مع عدة workers
   - فعّل caching للـ static files

4. **المراقبة:**
   - راقب السجلات بانتظام
   - استخدم خدمات مثل Sentry للأخطاء

---

## 🔄 التحديثات | Updates

لتحديث النظام بعد النشر:

```bash
# 1. على جهازك المحلي
git pull origin main

# 2. إذا كانت هناك تحديثات قاعدة بيانات
# أنشئ migration جديد في migrations/

# 3. push التغييرات
git push origin main

# 4. على السيرفر (إذا لزم)
python apply_migrations.py
```

---

## 📞 الدعم | Support

إذا واجهت مشاكل في النشر:

1. راجع السجلات (logs)
2. تحقق من المتغيرات البيئية
3. تأكد من تطبيق migrations
4. راجع هذا الدليل والوثائق الأخرى

---

**تم التجهيز للنشر السحابي! ✅**

**Ready for Cloud Deployment! 🚀**

---

**تاريخ:** 18 نوفمبر 2025  
**الإصدار:** 1.0.0
