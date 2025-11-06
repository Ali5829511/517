# قائمة التحقق من النشر | Deployment Checklist
# نظام إدارة الإسكان الجامعي

استخدم هذه القائمة للتأكد من أن كل شيء جاهز للنشر.
Use this checklist to ensure everything is ready for deployment.

---

## ✅ قبل النشر | Pre-Deployment

### الملفات الأساسية | Essential Files
- [x] `app.py` - التطبيق الرئيسي | Main application
- [x] `requirements.txt` - المتطلبات | Dependencies
- [x] `Procfile` - إعدادات Heroku/Railway | Heroku/Railway config
- [x] `runtime.txt` - نسخة Python | Python version
- [x] `render.yaml` - إعدادات Render | Render config
- [x] `railway.json` - إعدادات Railway | Railway config
- [x] `vercel.json` - إعدادات Vercel | Vercel config
- [x] `.env.example` - قالب المتغيرات | Variables template
- [x] `.gitignore` - ملفات التجاهل | Ignored files
- [x] `housing_database.db` - قاعدة البيانات | Database

### الوثائق | Documentation
- [x] `README.md` - نظرة عامة | Overview
- [x] `DEPLOYMENT.md` - دليل النشر الشامل | Comprehensive deployment guide
- [x] `DEPLOYMENT_GUIDE.md` - دليل النشر | Deployment guide
- [x] `DEPLOYMENT_UPDATE_OCT_2025.md` - آخر التحديثات | Latest updates
- [x] `RENDER_DEPLOYMENT.md` - دليل Render | Render guide
- [x] `DEPLOYMENT_CHECKLIST.md` - هذا الملف | This file

### البنية الأساسية | Basic Structure
- [x] المجلد `static/` موجود | `static/` folder exists
- [x] المجلد `uploads/` موجود | `uploads/` folder exists
- [x] المجلد `processed_images/` موجود | `processed_images/` folder exists
- [x] المجلد `logs/` موجود | `logs/` folder exists

---

## 🔧 الإعدادات | Configuration

### متغيرات البيئة المطلوبة | Required Environment Variables
- [ ] `FLASK_ENV=production` - بيئة الإنتاج | Production environment
- [ ] `SECRET_KEY` - مفتاح سري قوي | Strong secret key

### متغيرات البيئة الاختيارية | Optional Environment Variables
- [ ] `OPENAI_API_KEY` - لميزات الذكاء الاصطناعي | For AI features
- [ ] `FLASK_DEBUG=0` - إيقاف وضع التطوير | Disable debug mode

### التحقق من الإعدادات | Configuration Verification
- [ ] لا توجد مفاتيح API في الكود | No API keys in code
- [ ] جميع المتغيرات في `.env.example` | All variables in `.env.example`
- [ ] `DEBUG=False` في الإنتاج | `DEBUG=False` in production

---

## 🧪 الاختبار المحلي | Local Testing

### التشغيل المحلي | Local Run
```bash
# تثبيت المتطلبات | Install dependencies
pip install -r requirements.txt

# تشغيل التطبيق | Run application
python app.py

# أو باستخدام gunicorn | Or with gunicorn
gunicorn app:app --bind 127.0.0.1:8000
```

### اختبار النقاط النهائية | Test Endpoints
- [ ] `/` - الصفحة الرئيسية | Home page
- [ ] `/main_portal.html` - البوابة الرئيسية | Main portal
- [ ] `/api/statistics` - الإحصائيات | Statistics API
- [ ] `/static/comprehensive_system_report.html` - التقرير الشامل | Comprehensive report

### فحص الجودة | Quality Checks
```bash
# اختبار بناء التطبيق | Test build
./build.sh

# اختبار إعدادات النشر | Test deployment config
./deploy_test.sh

# فحص بناء الجملة | Syntax check
python -m py_compile app.py database_api.py
```

---

## 🚀 النشر على المنصات | Platform Deployment

### Railway.app (موصى به | Recommended)
- [ ] تسجيل الدخول باستخدام GitHub | Login with GitHub
- [ ] إنشاء مشروع جديد | Create new project
- [ ] اختيار المستودع | Select repository
- [ ] إضافة متغيرات البيئة | Add environment variables
- [ ] انتظار النشر التلقائي | Wait for auto-deployment
- [ ] اختبار الرابط | Test the URL

**الوقت المتوقع:** 3-5 دقائق | **Expected Time:** 3-5 minutes

### Render.com
- [ ] تسجيل الدخول | Login
- [ ] إنشاء Web Service | Create Web Service
- [ ] ربط GitHub | Connect GitHub
- [ ] تكوين الإعدادات من `render.yaml` | Configure from `render.yaml`
- [ ] إضافة متغيرات البيئة | Add environment variables
- [ ] النشر | Deploy
- [ ] اختبار الرابط | Test the URL

**الوقت المتوقع:** 5-10 دقائق | **Expected Time:** 5-10 minutes

### Vercel
- [ ] تثبيت Vercel CLI: `npm install -g vercel` | Install Vercel CLI
- [ ] تسجيل الدخول: `vercel login` | Login: `vercel login`
- [ ] النشر: `vercel --prod` | Deploy: `vercel --prod`
- [ ] إضافة متغيرات البيئة | Add environment variables
- [ ] اختبار الرابط | Test the URL

**الوقت المتوقع:** 2-3 دقائق | **Expected Time:** 2-3 minutes

### Heroku
- [ ] تثبيت Heroku CLI | Install Heroku CLI
- [ ] تسجيل الدخول: `heroku login` | Login: `heroku login`
- [ ] إنشاء التطبيق: `heroku create` | Create app: `heroku create`
- [ ] إضافة المتغيرات: `heroku config:set` | Add variables: `heroku config:set`
- [ ] الدفع: `git push heroku main` | Push: `git push heroku main`
- [ ] اختبار الرابط | Test the URL

**الوقت المتوقع:** 5-7 دقائق | **Expected Time:** 5-7 minutes

---

## ✅ بعد النشر | Post-Deployment

### التحقق من التشغيل | Verify Operation
- [ ] الصفحة الرئيسية تعمل | Home page works
- [ ] تسجيل الدخول يعمل | Login works
- [ ] البيانات تُعرض بشكل صحيح | Data displays correctly
- [ ] الصور تُحمل | Images load
- [ ] APIs تعمل | APIs work
- [ ] التقارير تُنشأ | Reports generate
- [ ] الرسوم البيانية تظهر | Charts display

### الأداء | Performance
- [ ] وقت التحميل < 3 ثواني | Load time < 3 seconds
- [ ] الاستجابة سريعة | Response is fast
- [ ] لا توجد أخطاء في Console | No console errors
- [ ] الذاكرة مستقرة | Memory stable

### الأمان | Security
- [ ] HTTPS مفعّل | HTTPS enabled
- [ ] لا توجد مفاتيح مكشوفة | No exposed keys
- [ ] رسائل الخطأ آمنة | Safe error messages
- [ ] CORS مضبوط بشكل صحيح | CORS properly configured

### المراقبة | Monitoring
- [ ] إعداد تنبيهات الأخطاء | Setup error alerts
- [ ] مراقبة السجلات | Monitor logs
- [ ] تتبع الاستخدام | Track usage
- [ ] فحص الأداء | Check performance

---

## 📊 اختبار الميزات | Feature Testing

### الوظائف الأساسية | Core Functions
- [ ] إدارة السكان | Residents management
- [ ] إدارة المباني | Buildings management
- [ ] إدارة الوحدات | Units management
- [ ] إدارة الملصقات | Stickers management
- [ ] إدارة المواقف | Parking management

### التقارير | Reports
- [ ] التقرير الشامل | Comprehensive report
- [ ] تقرير السكان | Residents report
- [ ] تقرير المباني | Buildings report
- [ ] تقرير الملصقات | Stickers report
- [ ] تقرير المواقف | Parking report

### ميزات الذكاء الاصطناعي | AI Features (إذا تم تفعيل OPENAI_API_KEY)
- [ ] التعرف على اللوحات | Plate recognition
- [ ] معالجة الصور | Image processing
- [ ] البحث الذكي | Smart search

---

## 🔍 حل المشاكل | Troubleshooting

### إذا فشل النشر | If Deployment Fails
1. تحقق من السجلات | Check logs:
   ```bash
   heroku logs --tail    # Heroku
   railway logs          # Railway
   vercel logs          # Vercel
   ```

2. تحقق من المتطلبات | Verify requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. تحقق من بناء الجملة | Check syntax:
   ```bash
   python -m py_compile app.py
   ```

4. شغل محلياً أولاً | Run locally first:
   ```bash
   python app.py
   ```

### الأخطاء الشائعة | Common Errors

**خطأ: Module not found**
```bash
# الحل | Solution
pip install <module-name>
# ثم أضفه إلى requirements.txt | Then add to requirements.txt
```

**خطأ: Port already in use**
```bash
# الحل | Solution
# غير PORT في الإعدادات | Change PORT in settings
export PORT=8080
```

**خطأ: Database not found**
```bash
# الحل | Solution
python generate_database.py
```

**خطأ: OPENAI_API_KEY invalid**
```bash
# الحل | Solution
# تحقق من صحة المفتاح | Verify key is correct
# النظام يعمل بدون المفتاح | System works without key
```

---

## 📞 الدعم | Support

### الوثائق | Documentation
- 📘 [DEPLOYMENT.md](DEPLOYMENT.md) - دليل شامل | Comprehensive guide
- 📗 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - دليل أساسي | Basic guide
- 📙 [README.md](README.md) - نظرة عامة | Overview

### المساعدة | Help
- 🌐 GitHub Issues: https://github.com/Ali5829511/517/issues
- 📧 Email: housing@imamu.edu.sa

### الأدوات المفيدة | Useful Tools
- [Railway CLI](https://docs.railway.app/develop/cli)
- [Render Dashboard](https://dashboard.render.com)
- [Vercel CLI](https://vercel.com/docs/cli)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

---

## ✅ اكتمال النشر | Deployment Complete

عند اكتمال جميع الخطوات أعلاه، يكون النظام جاهزاً للاستخدام!

When all steps above are complete, the system is ready for use!

**تاريخ النشر | Deployment Date:** __________

**المنصة | Platform:** __________

**الرابط | URL:** __________

**ملاحظات | Notes:**
___________________________________
___________________________________
___________________________________

---

© 2025 جامعة الإمام محمد بن سعود الإسلامية  
© 2025 Imam Muhammad bin Saud Islamic University

**الحالة:** جاهز للنشر ✅  
**Status:** Ready for Deployment ✅
