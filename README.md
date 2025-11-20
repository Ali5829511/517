# نظام إدارة الإسكان الجامعي

نظام متكامل لإدارة إسكان أعضاء هيئة التدريس مع ميزات الذكاء الاصطناعي

## 📚 التوثيق الشامل - Comprehensive Documentation

**🆕 وثائق نظام التعرف على اللوحات (18 نوفمبر 2025):**
- 🚗 **[PLATE_RECOGNITION_GUIDE.md](PLATE_RECOGNITION_GUIDE.md)** - **دليل شامل لنظام التعرف على اللوحات**
- ⚡ **[plate_recognition/QUICKSTART.md](plate_recognition/QUICKSTART.md)** - تشغيل سريع في خطوة واحدة
- 📖 **[plate_recognition/README.md](plate_recognition/README.md)** - توثيق تفصيلي كامل
- 💡 **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - أمثلة عملية شاملة (curl, Python, سيناريوهات)

**وثائق النظام الأساسي (17 نوفمبر 2025):**
- ⭐ **[COMPREHENSIVE_FINAL_SUMMARY.md](COMPREHENSIVE_FINAL_SUMMARY.md)** - الملخص النهائي الشامل
- 📖 **[QUICK_USE_GUIDE.md](QUICK_USE_GUIDE.md)** - دليل الاستخدام السريع
- 📊 **[COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md)** - تقرير شامل عن حالة المشروع
- 🔒 **[SECURITY_NOTES.md](SECURITY_NOTES.md)** - ملاحظات أمنية مفصلة
- 📑 **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - فهرس شامل لجميع الوثائق

## 🚀 التشغيل السريع

### نظام إدارة الإسكان (Flask)
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-your-key-here"  # اختياري
python app.py
# افتح: http://localhost:5000
```

### نظام التعرف على اللوحات (FastAPI) 🆕
```bash
./run_plate_system.sh
# أو: cd plate_recognition && uvicorn main:app --reload
# افتح: http://localhost:8000
# التوثيق: http://localhost:8000/docs
```

### المتطلبات
- Python 3.11+
- مفتاح OpenAI API (اختياري للميزات الذكية)
- رمز GitHub PAT (اختياري لتكامل GitHub)

⚠️ **تحذير أمني**: لا تشارك المفاتيح السرية أو الرموز. احفظها في متغيرات البيئة فقط.

## 📊 قاعدة البيانات
- 165 مبنى
- 1,134 وحدة سكنية
- 1,057 ساكن
- 2,381 ملصق سيارة
- 1,308 موقف

## 🆕 آخر التحديثات

### 18 نوفمبر 2025 - نظام التعرف على اللوحات المرورية 🚗⭐
- ✅ **نظام FastAPI متكامل** للتعرف على اللوحات وتتبع المخالفات
- ✅ **4 جداول قاعدة بيانات** (vehicles, cameras, events, violations)
- ✅ **API شامل** مع 9 endpoints (webhook, events, violations, export, import)
- ✅ **تتبع مخالفات تلقائي** (التكرار، الدخول غير المصرح)
- ✅ **تصدير/استيراد** (Excel, PDF, HTML)
- ✅ **واجهة عربية احترافية** مع Bootstrap 5
- ✅ **11 اختبار شامل** (100% نجاح)
- ✅ **توثيق كامل** (4 ملفات جديدة)
- 📖 راجع: [PLATE_RECOGNITION_GUIDE.md](PLATE_RECOGNITION_GUIDE.md)

### 4 نوفمبر 2025 - تحديث التوثيق والأمان ⭐
- ✅ إضافة توثيق شامل جديد (4 ملفات)
- ✅ تحذيرات أمنية مفصلة
- ✅ دليل استخدام سريع وعملي
- ✅ فهرس شامل لجميع الوثائق
- ✅ مراجعة كود كاملة (Code Review)

### 30 أكتوبر 2025 - تحسينات الجودة
- ✅ إصلاح 343 مشكلة جودة كود
- ✅ إصلاح 20 ثغرة أمنية
- ✅ نظام تقارير شامل تفاعلي
- ✅ 8 رسوم بيانية متقدمة

## 🌐 النشر | Deployment

النظام جاهز للنشر على منصات متعددة:
- **Railway.app** 🏆 (موصى به) - نشر تلقائي في 2-3 دقائق
- **Render.com** (للإنتاج) - موثوقية عالية
- **Heroku** (الكلاسيكي) - الأكثر شهرة
- **Vercel** (Serverless) - نشر سريع
- **Google Cloud Run** (حاويات) - مرونة عالية
- **AWS Elastic Beanstalk** - تكامل AWS
- **Azure App Service** - Microsoft Cloud
- **DigitalOcean** - بسيط وقوي
- **XAMPP** (محلي) - للتطوير والاختبار المحلي

### 📖 أدلة النشر | Deployment Guides

#### 🆕 أدلة جديدة وشاملة | New Comprehensive Guides
- ⭐ **[CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md)** - **دليل النشر السحابي الشامل لـ 8 منصات** 🆕
  - خطوات مفصلة لكل منصة
  - أمثلة أوامر قابلة للتنفيذ
  - استكشاف الأخطاء وحلولها
  - إرشادات الأمان والأداء
- 🚀 **[CLOUD_DEPLOYMENT_QUICKSTART.md](CLOUD_DEPLOYMENT_QUICKSTART.md)** - **دليل البدء السريع** 🆕
  - أزرار النشر بنقرة واحدة
  - مقارنة المنصات
  - نصائح النجاح
- 🇸🇦 **[DEPLOYMENT_GUIDE_AR.md](DEPLOYMENT_GUIDE_AR.md)** - **دليل النشر بالعربية** 🆕
  - شرح مبسط للمبتدئين
  - خطوات واضحة ومفصلة
  - حل المشاكل الشائعة

#### ملفات التكوين الجاهزة | Ready Configuration Files
- ✅ `Procfile` - Heroku, Railway
- ✅ `app.json` - Heroku one-click deploy
- ✅ `railway.json` - Railway configuration
- ✅ `render.yaml` - Render configuration
- ✅ `vercel.json` - Vercel configuration
- ✅ `app.yaml` - Google Cloud App Engine
- ✅ `azure-pipelines.yml` - Azure DevOps
- ✅ `.do/app.yaml` - DigitalOcean App Platform
- ✅ `Dockerfile` - Docker/Cloud Run

#### أدلة أخرى | Other Guides
- [XAMPP_QUICK_START.md](XAMPP_QUICK_START.md) - دليل سريع للتشغيل على XAMPP
- [XAMPP_DEPLOYMENT.md](XAMPP_DEPLOYMENT.md) - دليل XAMPP الشامل
- [DEPLOYMENT.md](DEPLOYMENT.md) - دليل النشر الشامل (نسخة سابقة)
- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - النشر في 3 دقائق

### 🚀 النشر السريع | Quick Deploy

#### نشر بنقرة واحدة | One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Ali5829511/517)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Ali5829511/517)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Ali5829511/517)

### ⚡ خطوات سريعة للنشر على Railway (موصى به):
1. سجل على https://railway.app
2. اربط GitHub repo: Ali5829511/517
3. أضف متغيرات البيئة (اختياري):
   - `OPENAI_API_KEY` (للميزات الذكية)
4. سيتم النشر تلقائياً في 2-3 دقائق ✅

### 📋 خطوات سريعة للنشر على Render:
1. سجل على https://render.com
2. New + → Web Service
3. اربط GitHub repo: Ali5829511/517
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120`
6. انتظر النشر (5-10 دقائق) ✅

### 💻 خطوات سريعة للنشر على XAMPP (محلي):
1. ثبّت XAMPP و Python 3.11+
2. انسخ المشروع إلى `C:\xampp\htdocs\housing-system`
3. نفذ `pip install -r requirements.txt`
4. شغّل `start_flask_windows.bat`
5. افتح `http://127.0.0.1:5000` ✅

📚 للتفاصيل الكاملة، راجع:
- [CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md) - الدليل الشامل
- [CLOUD_DEPLOYMENT_QUICKSTART.md](CLOUD_DEPLOYMENT_QUICKSTART.md) - البدء السريع
- [DEPLOYMENT_GUIDE_AR.md](DEPLOYMENT_GUIDE_AR.md) - دليل عربي مبسط

تم التطوير بواسطة Manus AI

**شارك في تأليف:**
Co-authored-by: Ali5829511 <132597948+Ali5829511@users.noreply.github.com>

HWGP - Housing Management System Project
