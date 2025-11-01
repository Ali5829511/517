# دليل البدء السريع - XAMPP
# XAMPP Quick Start Guide

## 🚀 البدء السريع في 5 دقائق

### الخطوة 1: تثبيت المتطلبات (5 دقائق)

#### 1.1 تثبيت XAMPP
- حمّل من: https://www.apachefriends.org/download.html
- ثبّت في المسار الافتراضي:
  - **Windows:** `C:\xampp`
  - **Linux:** `/opt/lampp`

#### 1.2 تثبيت Python 3.11+
- حمّل من: https://www.python.org/downloads/
- **مهم:** حدد "Add Python to PATH" أثناء التثبيت

---

### الخطوة 2: إعداد المشروع (دقيقتان)

#### 2.1 نسخ الملفات
انسخ مجلد المشروع إلى:
- **Windows:** `C:\xampp\htdocs\housing-system`
- **Linux:** `/opt/lampp/htdocs/housing-system`

#### 2.2 تثبيت المكتبات
افتح Command Prompt / Terminal:
```bash
cd C:\xampp\htdocs\housing-system
pip install -r requirements.txt
```

---

### الخطوة 3: إعداد ملف البيئة (دقيقة واحدة)

أنشئ ملف `.env` في مجلد المشروع:
```env
OPENAI_API_KEY=your-api-key-here
FLASK_ENV=production
SECRET_KEY=your-secret-key-change-this
DATABASE_PATH=housing_database.db
HOST=127.0.0.1
PORT=5000
```

**ملاحظة:** احصل على OpenAI API Key من: https://platform.openai.com/api-keys

---

### الخطوة 4: تشغيل التطبيق (دقيقة واحدة)

#### الطريقة السهلة - تشغيل مباشر:

**Windows:**
```bash
# انقر نقراً مزدوجاً على:
start_flask_windows.bat
```

**Linux:**
```bash
# في Terminal:
./start_flask_linux.sh
```

#### أو يدوياً:
```bash
cd C:\xampp\htdocs\housing-system
python app.py
```

---

### الخطوة 5: الوصول إلى التطبيق

افتح المتصفح وانتقل إلى:
```
http://127.0.0.1:5000
```

**تسجيل الدخول:**
- اسم المستخدم: `admin`
- كلمة المرور: `Admin@2025`

---

## 🎯 استخدام Apache (اختياري - للنشر)

إذا أردت استخدام Apache بدلاً من تشغيل Flask مباشرة:

### 1. تفعيل وحدات Apache
افتح `C:\xampp\apache\conf\httpd.conf` وتأكد من إلغاء التعليق عن:
```apache
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so
```

### 2. إضافة Virtual Host
أضف في نهاية `httpd.conf`:
```apache
<VirtualHost *:80>
    ServerName housing.local
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
</VirtualHost>
```

### 3. تحديث ملف hosts
أضف في `C:\Windows\System32\drivers\etc\hosts`:
```
127.0.0.1    housing.local
```

### 4. إعادة تشغيل Apache
من XAMPP Control Panel، أعد تشغيل Apache

### 5. الوصول
افتح: `http://housing.local`

---

## ✅ التحقق من التثبيت

### اختبار 1: الصفحة الرئيسية
```
http://127.0.0.1:5000
```
يجب أن تظهر لوحة تحكم النظام

### اختبار 2: API
```
http://127.0.0.1:5000/api/statistics
```
يجب أن تظهر إحصائيات JSON

### اختبار 3: الملفات الثابتة
```
http://127.0.0.1:5000/static/login.html
```
يجب أن تظهر صفحة تسجيل الدخول

---

## 🐛 حل المشاكل السريعة

### المشكلة: "Python not found"
**الحل:**
```bash
# تحقق من تثبيت Python
python --version
# إذا لم يعمل، أضف Python إلى PATH
```

### المشكلة: "Port 5000 already in use"
**الحل:**
```bash
# غيّر المنفذ في ملف .env:
PORT=8000
```

### المشكلة: "Module not found"
**الحل:**
```bash
pip install -r requirements.txt
```

### المشكلة: قاعدة البيانات لا تعمل
**الحل:**
```bash
# تحقق من وجود ملف قاعدة البيانات
dir housing_database.db    # Windows
ls -l housing_database.db  # Linux
```

### المشكلة: Apache لا يعمل (Port 80)
**الحل:**
- أغلق Skype أو أي برنامج يستخدم المنفذ 80
- أو غيّر منفذ Apache في XAMPP Config

---

## 🔥 تشغيل مع Gunicorn (موصى به للإنتاج)

### Windows:
```bash
start_gunicorn_windows.bat
```

### Linux:
```bash
./start_gunicorn_linux.sh
```

---

## 📊 الإحصائيات

بعد التشغيل، يمكنك رؤية:
- **165** مبنى
- **1,134** وحدة سكنية
- **1,057** ساكن
- **2,381** ملصق سيارة

---

## 🆘 الحصول على المساعدة

### السجلات (Logs)
تحقق من:
```
logs/housing-error.log
logs/gunicorn-error.log
```

### الوثائق الكاملة
راجع `XAMPP_DEPLOYMENT.md` للتفاصيل الكاملة

### اختبار البيئة
```bash
python --version
pip list
python -c "from app import app; print('App loaded successfully')"
```

---

## 📱 الوصول من أجهزة أخرى

### 1. اعرف عنوان IP الخاص بك:

**Windows:**
```bash
ipconfig
```
ابحث عن "IPv4 Address"

**Linux:**
```bash
ip addr show
```

### 2. غيّر HOST في `.env`:
```env
HOST=0.0.0.0
```

### 3. افتح الجدار الناري:
**Windows:** Windows Firewall → Allow an app → أضف Python

**Linux:**
```bash
sudo ufw allow 5000
```

### 4. الوصول من جهاز آخر:
```
http://YOUR_IP_ADDRESS:5000
```

---

## 🎓 المعلومات

- **المؤسسة:** جامعة الإمام محمد بن سعود الإسلامية
- **النظام:** نظام إدارة الإسكان الجامعي
- **التقنيات:** Flask, Python, SQLite, OpenAI

---

## ✨ الميزات

- ✅ إدارة السكان وأعضاء هيئة التدريس
- ✅ إدارة المباني والوحدات السكنية
- ✅ نظام ملصقات السيارات
- ✅ استخراج اللوحات بالذكاء الاصطناعي (OpenAI Vision)
- ✅ تقارير شاملة ومتقدمة
- ✅ واجهة عربية كاملة

---

## 🔐 الأمان

⚠️ **تحذيرات أمنية:**
- لا تشارك ملف `.env` مع أحد
- غيّر `SECRET_KEY` في الإنتاج
- استخدم HTTPS في الإنتاج
- احفظ نسخة احتياطية من قاعدة البيانات

---

تم بواسطة GitHub Copilot | © 2025 جامعة الإمام
