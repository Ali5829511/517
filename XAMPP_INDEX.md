# فهرس ملفات XAMPP - XAMPP Files Index

## 📚 دليل سريع لجميع ملفات وتوثيقات XAMPP

هذا الملف يوفر نظرة شاملة على جميع الملفات المتعلقة بتشغيل المشروع على XAMPP.

---

## 🎯 البدء السريع

**للمستخدمين الجدد - ابدأ من هنا:**

1. 🌟 [README_XAMPP_AR.md](README_XAMPP_AR.md) - **الدليل الشامل بالعربية** (مُوصى به)
   - دليل كامل من الألف إلى الياء
   - شرح مفصل بالعربية
   - أمثلة وصور توضيحية

2. ⚡ [XAMPP_QUICK_START.md](XAMPP_QUICK_START.md) - **البدء السريع** (5 دقائق)
   - للتشغيل السريع
   - خطوات مختصرة
   - حل المشاكل الشائعة

---

## 📖 التوثيق الكامل

### الأدلة الرئيسية

| الملف | الوصف | المحتوى | الحجم |
|------|--------|---------|-------|
| [README_XAMPP_AR.md](README_XAMPP_AR.md) | 🇸🇦 دليل شامل بالعربية | شرح كامل من التثبيت للتشغيل | 14 KB |
| [XAMPP_DEPLOYMENT.md](XAMPP_DEPLOYMENT.md) | 🌐 دليل النشر الكامل | طرق متعددة، HTTPS، الإنتاج | 12 KB |
| [XAMPP_QUICK_START.md](XAMPP_QUICK_START.md) | ⚡ البدء السريع | 5 دقائق للتشغيل | 6.2 KB |
| [XAMPP_SETUP_CHECKLIST.md](XAMPP_SETUP_CHECKLIST.md) | ✅ قائمة التحقق | خطوة بخطوة للتحقق | 11 KB |

### محتويات كل دليل

#### 1. README_XAMPP_AR.md (الدليل الأساسي) 🌟
```
✅ نظرة عامة عن XAMPP
✅ التثبيت السريع (10 دقائق)
✅ تحضير المشروع
✅ اختبار التثبيت
✅ تشغيل النظام
✅ الإعداد المتقدم
✅ دليل الاستخدام السريع
✅ حل المشاكل الشائعة
✅ الأمان والخصوصية
✅ الوصول من أجهزة أخرى
```

#### 2. XAMPP_DEPLOYMENT.md (للمحترفين)
```
✅ الطريقة 1: Flask مع Apache (Reverse Proxy)
✅ الطريقة 2: mod_wsgi
✅ تشغيل Flask كخدمة (Windows & Linux)
✅ استخدام Gunicorn
✅ إعداد HTTPS
✅ الأمان في الإنتاج
✅ تحسين الأداء
```

#### 3. XAMPP_QUICK_START.md (للمستعجلين)
```
✅ خطوات سريعة
✅ تثبيت المتطلبات
✅ إعداد وتشغيل
✅ الوصول للنظام
✅ حل المشاكل السريع
```

#### 4. XAMPP_SETUP_CHECKLIST.md (للدقيقين)
```
✅ قائمة فحص كاملة
✅ التحقق من المتطلبات
✅ خطوات التثبيت
✅ الاختبارات الوظيفية
✅ فحص الأمان
✅ التحقق النهائي
```

---

## 🔧 ملفات التكوين

### ملفات Apache

| الملف | الاستخدام | الوصف |
|------|-----------|--------|
| [.htaccess](.htaccess) | حماية وتوجيه | إعدادات Apache، حماية الملفات |
| [apache_vhost_config.conf](apache_vhost_config.conf) | Virtual Host | نموذج تكوين Apache كامل |

### ملفات Python

| الملف | الاستخدام | الوصف |
|------|-----------|--------|
| [housing.wsgi](housing.wsgi) | mod_wsgi | ملف WSGI للتشغيل مع Apache |
| [housing-flask.service](housing-flask.service) | Systemd | خدمة Linux للتشغيل التلقائي |

---

## 🚀 سكريبتات التشغيل

### للتشغيل المباشر (Flask Development Server)

#### Windows
```batch
start_flask_windows.bat
```
- ✅ تحميل متغيرات البيئة
- ✅ فحص Python
- ✅ فحص قاعدة البيانات
- ✅ تشغيل Flask

#### Linux
```bash
./start_flask_linux.sh
```
- ✅ تحميل متغيرات البيئة
- ✅ فحص Python3
- ✅ ضبط الصلاحيات
- ✅ تشغيل Flask

### للإنتاج (Gunicorn)

#### Windows
```batch
start_gunicorn_windows.bat
```
- ✅ 4 workers
- ✅ Timeout 120s
- ✅ تسجيل السجلات

#### Linux
```bash
./start_gunicorn_linux.sh
```
- ✅ 4 workers
- ✅ Timeout 120s
- ✅ تسجيل السجلات

---

## 🧪 أدوات الاختبار

### test_xampp_setup.py - سكريبت الاختبار الشامل

**الاستخدام:**
```bash
python test_xampp_setup.py
```

**الاختبارات:**
- ✅ إصدار Python (3.11+)
- ✅ المكتبات المطلوبة
- ✅ ملفات المشروع
- ✅ ملف .env
- ✅ استيراد التطبيق
- ✅ قاعدة البيانات
- ✅ توفر المنفذ 5000

**الإخراج:**
- ✅ رسائل ملونة
- ✅ تقرير مفصل
- ✅ اقتراحات للحلول
- ✅ ملخص نهائي

---

## 📊 مخطط التشغيل

```
┌─────────────────────────────────────────────┐
│  اختر طريقة التشغيل                         │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│  مباشر       │        │  مع Apache   │
│  Direct      │        │  With Apache │
└──────────────┘        └──────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│ Flask Dev    │        │ Reverse      │
│ Server       │        │ Proxy        │
│              │        │              │
│ أو           │        │ أو           │
│              │        │              │
│ Gunicorn     │        │ mod_wsgi     │
└──────────────┘        └──────────────┘
        │                       │
        └───────────┬───────────┘
                    ▼
        ┌────────────────────┐
        │   المتصفح          │
        │   Browser          │
        └────────────────────┘
```

---

## 🎯 حالات الاستخدام

### الحالة 1: التطوير والاختبار (Development)
**الطريقة الموصى بها:**
```bash
# Windows
start_flask_windows.bat

# Linux
./start_flask_linux.sh
```
**المميزات:**
- ✅ سريع وسهل
- ✅ إعادة تحميل تلقائية
- ✅ رسائل خطأ مفصلة

### الحالة 2: الإنتاج المحلي (Local Production)
**الطريقة الموصى بها:**
```bash
# Windows
start_gunicorn_windows.bat

# Linux
./start_gunicorn_linux.sh
```
**المميزات:**
- ✅ أداء أفضل
- ✅ عدة workers
- ✅ استقرار عالي

### الحالة 3: الإنتاج مع Apache (Production with Apache)
**الطريقة الموصى بها:**
1. إعداد Apache Virtual Host
2. تشغيل Gunicorn
3. Apache يعمل كـ Reverse Proxy

**المميزات:**
- ✅ HTTPS
- ✅ Load Balancing
- ✅ تكامل كامل

---

## 🔒 الأمان

### الملفات المحمية
تم حماية الملفات التالية في `.htaccess`:
- ❌ `.env` - متغيرات البيئة
- ❌ `*.db` - قواعد البيانات
- ❌ `*.py` - ملفات Python
- ✅ `*.css, *.js, *.png` - الملفات الثابتة فقط

### Security Headers
تم تفعيل:
- ✅ X-Content-Type-Options
- ✅ X-Frame-Options
- ✅ X-XSS-Protection
- ✅ Referrer-Policy

---

## 📈 الأداء

### Flask Development Server
- استخدام: التطوير فقط
- Workers: 1
- Requests/second: ~100
- ⚠️ لا تستخدم في الإنتاج

### Gunicorn
- استخدام: الإنتاج
- Workers: 4 (قابل للتعديل)
- Requests/second: ~1000+
- ✅ موصى به للإنتاج

### Apache mod_wsgi
- استخدام: الإنتاج
- Threads: قابل للتعديل
- Requests/second: ~500-1000
- ✅ تكامل كامل مع Apache

---

## 🆘 حل المشاكل

### مرجع سريع

| المشكلة | الحل | الصفحة |
|---------|------|--------|
| Python not found | تثبيت Python + PATH | README_XAMPP_AR.md |
| Port in use | تغيير PORT | XAMPP_QUICK_START.md |
| Module not found | pip install | README_XAMPP_AR.md |
| Apache error | تفعيل modules | XAMPP_DEPLOYMENT.md |
| Database error | فحص الملف | XAMPP_SETUP_CHECKLIST.md |

---

## 📱 الوصول من الشبكة

### الخطوات:
1. غيّر `HOST=0.0.0.0` في `.env`
2. افتح الجدار الناري
3. استخدم IP الجهاز

**التفاصيل في:**
- README_XAMPP_AR.md (قسم "الوصول من أجهزة أخرى")
- XAMPP_QUICK_START.md (قسم "Access from other devices")

---

## 🔄 تحديثات وصيانة

### نسخ احتياطي
```bash
# قاعدة البيانات
copy housing_database.db backup/housing_database_$(date +%Y%m%d).db

# الملفات المرفوعة
copy -r uploads backup/uploads_$(date +%Y%m%d)
```

### تحديث المكتبات
```bash
pip install --upgrade -r requirements.txt
```

### مراقبة السجلات
```bash
# Flask logs
tail -f logs/housing-error.log

# Gunicorn logs
tail -f logs/gunicorn-error.log

# Apache logs
tail -f C:\xampp\apache\logs\error.log
```

---

## 📞 الدعم والمساعدة

### الوثائق
1. ابدأ بـ [README_XAMPP_AR.md](README_XAMPP_AR.md)
2. راجع [XAMPP_QUICK_START.md](XAMPP_QUICK_START.md)
3. استخدم [XAMPP_SETUP_CHECKLIST.md](XAMPP_SETUP_CHECKLIST.md)
4. للتفاصيل: [XAMPP_DEPLOYMENT.md](XAMPP_DEPLOYMENT.md)

### الاختبار
```bash
python test_xampp_setup.py
```

### السجلات
- `logs/housing-error.log`
- `logs/gunicorn-error.log`
- `C:\xampp\apache\logs\error.log`

---

## 🎓 معلومات إضافية

### الوثائق الأخرى
- [README.md](README.md) - معلومات المشروع
- [DEPLOYMENT.md](DEPLOYMENT.md) - نشر على السحابة
- [QUICK_START.md](QUICK_START.md) - بدء سريع عام

### الملفات الأساسية
- [app.py](app.py) - التطبيق الرئيسي
- [requirements.txt](requirements.txt) - المكتبات
- [config.py](config.py) - التكوين
- [database_api.py](database_api.py) - قاعدة البيانات

---

## ✨ ملخص سريع

### للمستخدمين الجدد
1. اقرأ [README_XAMPP_AR.md](README_XAMPP_AR.md)
2. نفذ [XAMPP_SETUP_CHECKLIST.md](XAMPP_SETUP_CHECKLIST.md)
3. شغّل `start_flask_windows.bat` أو `start_flask_linux.sh`
4. افتح http://127.0.0.1:5000

### للمحترفين
1. اقرأ [XAMPP_DEPLOYMENT.md](XAMPP_DEPLOYMENT.md)
2. اختر الطريقة المناسبة
3. طبّق التكوين
4. راقب الأداء

### للاختبار
```bash
python test_xampp_setup.py
```

---

## 🎉 تهانينا!

لديك الآن جميع الأدوات والوثائق اللازمة لتشغيل نظام إدارة الإسكان على XAMPP!

---

© 2025 جامعة الإمام محمد بن سعود الإسلامية  
تم إنشاء هذا الفهرس بواسطة GitHub Copilot
