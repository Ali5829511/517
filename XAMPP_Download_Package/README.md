# حزمة تشغيل نظام إدارة الإسكان على XAMPP
# XAMPP Deployment Package for Housing Management System

## 📦 محتويات الحزمة - Package Contents

هذه الحزمة تحتوي على جميع الملفات اللازمة لتشغيل نظام إدارة الإسكان الجامعي على خادم XAMPP.
This package contains all necessary files to run the Housing Management System on XAMPP server.

### 📚 المجلدات - Folders

```
XAMPP_Download_Package/
├── documentation/        # الوثائق - Documentation (5 guides)
├── configuration/        # ملفات التكوين - Configuration files (4 files)
├── scripts/             # سكريبتات التشغيل - Startup scripts (4 scripts)
├── tools/               # أدوات الاختبار - Testing tools
└── README.md           # هذا الملف - This file
```

---

## 🚀 دليل التثبيت السريع - Quick Installation Guide

### الخطوة 1: تحميل المشروع الأساسي
**Download the main project**

1. قم بتحميل المشروع الكامل من GitHub
2. استخرج الملفات إلى المجلد المطلوب

### الخطوة 2: نسخ ملفات XAMPP
**Copy XAMPP files**

انسخ محتويات هذه الحزمة إلى مجلد المشروع الرئيسي:
Copy the contents of this package to the main project folder:

```bash
# Windows
xcopy /E /I XAMPP_Download_Package\* C:\xampp\htdocs\housing-system\

# Linux
cp -r XAMPP_Download_Package/* /opt/lampp/htdocs/housing-system/
```

### الخطوة 3: التثبيت والإعداد
**Installation and Setup**

اتبع التعليمات في الوثائق:
Follow the instructions in the documentation:

1. **للمبتدئين - For Beginners**: 
   - اقرأ `documentation/README_XAMPP_AR.md`
   - Read `documentation/README_XAMPP_AR.md`

2. **للبدء السريع - For Quick Start**: 
   - اتبع `documentation/XAMPP_QUICK_START.md`
   - Follow `documentation/XAMPP_QUICK_START.md`

3. **للتحقق - For Verification**: 
   - استخدم `documentation/XAMPP_SETUP_CHECKLIST.md`
   - Use `documentation/XAMPP_SETUP_CHECKLIST.md`

---

## 📁 تفاصيل المحتويات - Contents Details

### 📚 documentation/ - الوثائق

| الملف | الوصف | الحجم |
|------|--------|-------|
| `README_XAMPP_AR.md` | دليل شامل بالعربية - Comprehensive Arabic guide | 14 KB |
| `XAMPP_DEPLOYMENT.md` | دليل النشر التقني - Technical deployment guide | 12 KB |
| `XAMPP_QUICK_START.md` | دليل البدء السريع - Quick start guide | 6 KB |
| `XAMPP_SETUP_CHECKLIST.md` | قائمة التحقق - Verification checklist | 11 KB |
| `XAMPP_INDEX.md` | فهرس الملفات - Navigation index | 12 KB |

**إجمالي الوثائق:** 55 KB من التعليمات الشاملة
**Total Documentation:** 55 KB of comprehensive instructions

### 🔧 configuration/ - ملفات التكوين

| الملف | الاستخدام | الوصف |
|------|-----------|--------|
| `.htaccess` | Apache | حماية الملفات والتوجيه - File protection & routing |
| `apache_vhost_config.conf` | Apache | تكوين Virtual Host - Virtual host configuration |
| `housing.wsgi` | mod_wsgi | نقطة دخول WSGI - WSGI entry point |
| `housing-flask.service` | Systemd | خدمة Linux - Linux service file |

**الاستخدام:** انسخ الملفات حسب طريقة النشر المختارة
**Usage:** Copy files according to your chosen deployment method

### 🚀 scripts/ - سكريبتات التشغيل

| السكريبت | المنصة | الوصف |
|---------|--------|--------|
| `start_flask_windows.bat` | Windows | تشغيل Flask - Start Flask server |
| `start_flask_linux.sh` | Linux | تشغيل Flask - Start Flask server |
| `start_gunicorn_windows.bat` | Windows | تشغيل Gunicorn - Start Gunicorn (production) |
| `start_gunicorn_linux.sh` | Linux | تشغيل Gunicorn - Start Gunicorn (production) |

**ميزات السكريبتات:**
- ✅ تحميل متغيرات البيئة تلقائياً
- ✅ فحص قاعدة البيانات
- ✅ معالجة الأخطاء
- ✅ رسائل بالعربية والإنجليزية

**Script Features:**
- ✅ Automatic environment loading
- ✅ Database validation
- ✅ Error handling
- ✅ Bilingual messages (Arabic/English)

### 🧪 tools/ - أدوات الاختبار

| الأداة | الوصف |
|-------|--------|
| `test_xampp_setup.py` | اختبار شامل للإعداد - Comprehensive setup validator |

**الاختبارات المتضمنة:**
- ✅ إصدار Python
- ✅ المكتبات المطلوبة
- ✅ ملفات المشروع
- ✅ قاعدة البيانات
- ✅ توفر المنفذ 5000

---

## 🎯 طرق التشغيل - Deployment Methods

### الطريقة 1: التشغيل المباشر (للتطوير)
**Method 1: Direct Run (Development)**

```bash
# Windows
scripts\start_flask_windows.bat

# Linux
./scripts/start_flask_linux.sh
```

### الطريقة 2: Apache Reverse Proxy (موصى بها)
**Method 2: Apache Reverse Proxy (Recommended)**

1. انسخ `configuration/apache_vhost_config.conf`
2. عدّل الإعدادات حسب نظامك
3. أضف إلى `httpd.conf`
4. شغّل Flask وأعد تشغيل Apache

### الطريقة 3: mod_wsgi (للإنتاج)
**Method 3: mod_wsgi (Production)**

1. استخدم `configuration/housing.wsgi`
2. اتبع التعليمات في `XAMPP_DEPLOYMENT.md`

---

## ✅ التحقق من التثبيت - Installation Verification

بعد النسخ، قم بتشغيل:
After copying, run:

```bash
python tools/test_xampp_setup.py
```

يجب أن ترى:
You should see:
- ✅ Python Version: PASSED
- ✅ Required Modules: PASSED
- ✅ Project Files: PASSED
- ✅ Database: PASSED
- ✅ Port Availability: PASSED

---

## 📋 المتطلبات - Requirements

### النظام - System
- **XAMPP** (Apache 2.4+)
- **Python** 3.11 أو أحدث
- **Windows** أو **Linux** أو **macOS**

### المكتبات - Python Packages
```bash
pip install -r requirements.txt
```

المكتبات الأساسية:
- Flask 3.0.0
- Gunicorn 21.2.0
- Pillow 11.0.0
- python-dotenv 1.0.1

---

## 🔐 الأمان - Security

### ملفات محمية - Protected Files
الملفات التالية محمية تلقائياً عبر `.htaccess`:
These files are automatically protected via `.htaccess`:
- `.env` (متغيرات البيئة)
- `*.db` (قواعد البيانات)
- `*.py` (ملفات Python)

### إعدادات الأمان - Security Headers
تم تفعيل:
Enabled:
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Referrer-Policy

---

## 🆘 حل المشاكل - Troubleshooting

### المشكلة: Python not found
**الحل:** تأكد من إضافة Python إلى PATH

### المشكلة: Port 5000 in use
**الحل:** غيّر PORT في ملف `.env`

### المشكلة: Module not found
**الحل:** 
```bash
pip install -r requirements.txt
```

### المشكلة: Database error
**الحل:** تأكد من وجود `housing_database.db`

---

## 📞 الدعم - Support

### الوثائق الكاملة
راجع ملفات `documentation/` للحصول على:
- دليل شامل بالعربية
- خطوات التثبيت المفصلة
- حل المشاكل الشائعة
- إعدادات متقدمة

### الاختبار
```bash
python tools/test_xampp_setup.py
```

---

## 🎓 معلومات المشروع - Project Information

**النظام:** نظام إدارة الإسكان الجامعي
**System:** Faculty Housing Management System

**المؤسسة:** جامعة الإمام محمد بن سعود الإسلامية
**Institution:** Imam Muhammad bin Saud Islamic University

**التقنيات:** Flask, Python, SQLite, OpenAI, Apache
**Technologies:** Flask, Python, SQLite, OpenAI, Apache

**قاعدة البيانات:**
- 165 مبنى - 165 buildings
- 1,134 وحدة سكنية - 1,134 residential units
- 1,057 ساكن - 1,057 residents
- 2,381 ملصق سيارة - 2,381 vehicle stickers

---

## 📝 خطوات البدء السريع - Quick Start Steps

### 5 دقائق للتشغيل - 5 Minutes to Run

1. ✅ **تثبيت XAMPP**
   - حمّل من: https://www.apachefriends.org/download.html

2. ✅ **تثبيت Python 3.11+**
   - حمّل من: https://www.python.org/downloads/

3. ✅ **نسخ المشروع**
   - انسخ إلى: `C:\xampp\htdocs\housing-system`

4. ✅ **تثبيت المكتبات**
   ```bash
   pip install -r requirements.txt
   ```

5. ✅ **إنشاء ملف .env**
   ```env
   OPENAI_API_KEY=your-key-here
   FLASK_ENV=production
   SECRET_KEY=your-secret
   DATABASE_PATH=housing_database.db
   HOST=127.0.0.1
   PORT=5000
   ```

6. ✅ **تشغيل النظام**
   ```bash
   # Windows
   scripts\start_flask_windows.bat
   
   # Linux
   ./scripts/start_flask_linux.sh
   ```

7. ✅ **الوصول للنظام**
   - افتح: http://127.0.0.1:5000
   - المستخدم: `admin`
   - كلمة المرور: `Admin@2025`

---

## 🎉 تم إنشاء الحزمة بنجاح!

جميع الملفات جاهزة للاستخدام. اتبع الخطوات أعلاه للبدء.
All files are ready to use. Follow the steps above to get started.

---

© 2025 جامعة الإمام محمد بن سعود الإسلامية
**تم التطوير بواسطة GitHub Copilot**
Developed with GitHub Copilot
