# دليل التشغيل المحلي والنسخ الاحتياطي
# Local Setup and Backup Guide

**التاريخ:** 7 نوفمبر 2024  
**Date:** November 7, 2024

---

## 📋 المحتويات - Contents

1. [النسخ الاحتياطي - Backup](#النسخ-الاحتياطي---backup)
2. [التشغيل المحلي - Local Setup](#التشغيل-المحلي---local-setup)
3. [استعادة النسخة الاحتياطية - Restore Backup](#استعادة-النسخة-الاحتياطية---restore-backup)
4. [استكشاف الأخطاء - Troubleshooting](#استكشاف-الأخطاء---troubleshooting)

---

## النسخ الاحتياطي - Backup

### طريقة 1: باستخدام السكريبت التلقائي (موصى به)

```bash
# على Linux/Mac
chmod +x backup_system.sh
./backup_system.sh

# على Windows (باستخدام Git Bash)
bash backup_system.sh
```

**ما يقوم به السكريبت:**
- ✅ نسخ جميع ملفات Python
- ✅ نسخ قاعدة البيانات
- ✅ نسخ ملفات التكوين
- ✅ نسخ ملفات البيانات (Excel, CSV)
- ✅ نسخ المجلدات (static, uploads, processed_images)
- ✅ نسخ الوثائق المهمة
- ✅ إنشاء ملف معلومات النسخة
- ✅ خيار الضغط (tar.gz)

**الموقع الافتراضي للنسخة:**
```
~/housing_system_backup_YYYYMMDD_HHMMSS/
```

---

### طريقة 2: النسخ اليدوي

#### على Windows:

```batch
REM إنشاء مجلد النسخة الاحتياطية
mkdir C:\Backups\housing_system_%date:~-4,4%%date:~-10,2%%date:~-7,2%

REM نسخ الملفات
xcopy /E /I /Y *.py C:\Backups\housing_system_%date:~-4,4%%date:~-10,2%%date:~-7,2%\
xcopy /E /I /Y *.db C:\Backups\housing_system_%date:~-4,4%%date:~-10,2%%date:~-7,2%\
xcopy /E /I /Y static C:\Backups\housing_system_%date:~-4,4%%date:~-10,2%%date:~-7,2%\static\
xcopy /E /I /Y *.md C:\Backups\housing_system_%date:~-4,4%%date:~-10,2%%date:~-7,2%\
```

#### على Linux/Mac:

```bash
# إنشاء مجلد النسخة الاحتياطية
BACKUP_DIR=~/housing_system_backup_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# نسخ الملفات
cp -r *.py *.db static *.md requirements.txt $BACKUP_DIR/
```

---

## التشغيل المحلي - Local Setup

### طريقة 1: باستخدام السكريبت التلقائي (موصى به)

```bash
# على Linux/Mac
chmod +x run_local.sh
./run_local.sh

# على Windows (باستخدام Git Bash)
bash run_local.sh
```

**ما يقوم به السكريبت:**
- ✅ التحقق من Python
- ✅ التحقق من قاعدة البيانات
- ✅ تثبيت المتطلبات
- ✅ إنشاء ملف .env
- ✅ إنشاء المجلدات المطلوبة
- ✅ تشغيل التطبيق

---

### طريقة 2: التشغيل اليدوي

#### الخطوة 1: التحقق من المتطلبات

```bash
# التحقق من Python (يجب أن يكون 3.11 أو أحدث)
python3 --version

# إذا لم يكن مثبتاً، حمله من:
# https://www.python.org/downloads/
```

#### الخطوة 2: تثبيت المتطلبات

```bash
# تثبيت المكتبات المطلوبة
pip3 install -r requirements.txt

# أو على Windows
pip install -r requirements.txt
```

#### الخطوة 3: إعداد البيئة

```bash
# نسخ ملف .env.example
cp .env.example .env

# تعديل ملف .env وإضافة المفاتيح:
# SECRET_KEY=your-secret-key-here
# OPENAI_API_KEY=sk-your-openai-key (اختياري)
```

#### الخطوة 4: إنشاء المجلدات

```bash
mkdir -p uploads processed_images logs
```

#### الخطوة 5: تشغيل التطبيق

##### على Linux/Mac:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python3 app.py
```

##### على Windows:
```batch
set FLASK_ENV=development
set FLASK_DEBUG=1
python app.py
```

#### الخطوة 6: فتح المتصفح

افتح أحد العناوين التالية:
- http://localhost:5000
- http://127.0.0.1:5000

---

## استعادة النسخة الاحتياطية - Restore Backup

### من مجلد غير مضغوط:

```bash
# نسخ جميع الملفات إلى مجلد جديد
cp -r ~/housing_system_backup_YYYYMMDD_HHMMSS/* /path/to/new/location/

# الانتقال إلى المجلد الجديد
cd /path/to/new/location/

# تثبيت المتطلبات
pip3 install -r requirements.txt

# تشغيل التطبيق
python3 app.py
```

### من أرشيف مضغوط:

```bash
# فك الضغط
tar -xzf housing_system_backup_YYYYMMDD_HHMMSS.tar.gz

# الانتقال إلى المجلد
cd housing_system_backup_YYYYMMDD_HHMMSS

# تثبيت المتطلبات
pip3 install -r requirements.txt

# تشغيل التطبيق
python3 app.py
```

---

## استكشاف الأخطاء - Troubleshooting

### المشكلة 1: Python غير موجود

**الأعراض:**
```
command not found: python3
```

**الحل:**
1. حمّل Python من https://www.python.org/downloads/
2. تأكد من تحديد "Add Python to PATH" أثناء التثبيت
3. أعد تشغيل Terminal/CMD

---

### المشكلة 2: pip غير موجود

**الأعراض:**
```
command not found: pip
```

**الحل:**
```bash
# على Linux/Mac
python3 -m ensurepip --upgrade

# على Windows
python -m ensurepip --upgrade
```

---

### المشكلة 3: خطأ في تثبيت المتطلبات

**الأعراض:**
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**الحل (Windows):**
1. حمّل Microsoft C++ Build Tools
2. أو استخدم نسخة pre-built: `pip install --only-binary :all: package-name`

**الحل (Linux):**
```bash
sudo apt-get install python3-dev build-essential
```

---

### المشكلة 4: المنفذ مستخدم

**الأعراض:**
```
OSError: [Errno 48] Address already in use
```

**الحل:**
```bash
# إيقاف العملية على المنفذ 5000
# على Linux/Mac
lsof -ti:5000 | xargs kill -9

# على Windows
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F

# أو استخدم منفذ مختلف
export PORT=8000
python3 app.py
```

---

### المشكلة 5: قاعدة البيانات مفقودة

**الأعراض:**
```
sqlite3.OperationalError: no such table: residents
```

**الحل:**
```bash
# إنشاء قاعدة بيانات جديدة
python3 generate_database.py
```

---

### المشكلة 6: OpenAI API لا يعمل

**الأعراض:**
```
WARNING: OPENAI_API_KEY not found
```

**الحل:**
هذا تحذير فقط، النظام سيعمل بدون OpenAI. لتفعيله:
1. افتح `.env`
2. أضف: `OPENAI_API_KEY=sk-your-actual-key`
3. أعد تشغيل التطبيق

---

## 📊 فحص حالة النظام - System Health Check

### فحص سريع:

```bash
# التحقق من Python
python3 --version

# التحقق من المكتبات
pip3 list | grep Flask

# التحقق من قاعدة البيانات
sqlite3 housing_database.db "SELECT COUNT(*) FROM residents;"

# تشغيل الاختبارات
python3 -m pytest test_app.py -v
```

### النتيجة المتوقعة:
```
✓ Python 3.11+ installed
✓ Flask 3.0.0 installed
✓ Database has 1057 residents
✓ All tests passed (17/17)
```

---

## 🚀 أوامر مفيدة - Useful Commands

### تشغيل التطبيق في وضع الإنتاج:

```bash
# باستخدام Gunicorn (موصى به للإنتاج)
gunicorn app:app --bind 0.0.0.0:8000 --workers 4

# مع إعادة التشغيل التلقائي
gunicorn app:app --bind 0.0.0.0:8000 --workers 4 --reload
```

### تشغيل الاختبارات:

```bash
# جميع الاختبارات
python3 -m pytest test_app.py test_development_setup.py -v

# مع تغطية الكود
python3 -m pytest --cov=. --cov-report=html

# اختبار محدد
python3 -m pytest test_app.py::test_app_exists -v
```

### فحص جودة الكود:

```bash
# Flake8
flake8 app.py database_api.py --max-line-length=100

# Black (تنسيق تلقائي)
black app.py database_api.py --line-length=100
```

---

## 📝 ملاحظات مهمة - Important Notes

### الأمان:
1. ⚠️ **لا تشارك ملف .env** - يحتوي على مفاتيح سرية
2. ⚠️ **لا تضع النسخة الاحتياطية على GitHub** - قد تحتوي على بيانات حساسة
3. ✅ استخدم .gitignore لاستثناء .env

### الأداء:
1. للتطوير: استخدم `python app.py`
2. للإنتاج: استخدم `gunicorn`
3. للأداء الأفضل: زد عدد workers في gunicorn

### النسخ الاحتياطي:
1. احتفظ بنسخ احتياطية منتظمة (يومية/أسبوعية)
2. احفظ النسخ في مواقع متعددة
3. اختبر النسخة الاحتياطية بشكل دوري

---

## 📞 الدعم - Support

### إذا واجهت مشاكل:

1. **راجع الوثائق:**
   - README.md
   - DEPLOYMENT.md
   - SYSTEM_REVIEW_REPORT.md

2. **افحص السجلات:**
   - logs/app.log
   - التحقق من console output

3. **اختبر المكونات:**
   - قاعدة البيانات: `sqlite3 housing_database.db`
   - الاختبارات: `pytest -v`

---

## ✅ قائمة التحقق - Checklist

قبل التشغيل، تأكد من:

- [ ] Python 3.11+ مثبت
- [ ] pip مثبت
- [ ] المتطلبات مثبتة (`pip install -r requirements.txt`)
- [ ] ملف .env موجود ومعبأ
- [ ] قاعدة البيانات موجودة (housing_database.db)
- [ ] المجلدات المطلوبة موجودة (uploads/, processed_images/, logs/)
- [ ] المنفذ 5000 متاح (أو منفذ آخر)
- [ ] جدار الحماية يسمح بالاتصالات المحلية

---

**تم إعداد هذا الدليل - Guide Prepared**  
**التاريخ:** 7 نوفمبر 2024  
**Date:** November 7, 2024

✅ **النظام جاهز للتشغيل المحلي!**  
✅ **System ready for local deployment!**
