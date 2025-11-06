# دليل تشغيل المشروع على XAMPP
# Running the Project on XAMPP Server

## 📋 نظرة عامة - Overview

هذا الدليل يشرح كيفية تشغيل نظام إدارة الإسكان الجامعي على XAMPP.
This guide explains how to run the Faculty Housing Management System on XAMPP.

**ملاحظة مهمة:** XAMPP مصمم أساساً لتطبيقات PHP، لكن يمكن استخدامه لتشغيل تطبيقات Python Flask بطرق متعددة.
**Important Note:** XAMPP is primarily designed for PHP applications, but can be used to run Python Flask applications through multiple methods.

---

## 🎯 الطرق المتاحة - Available Methods

### الطريقة 1: تشغيل Flask مع Apache كخادم عكسي (موصى بها)
### Method 1: Run Flask with Apache as Reverse Proxy (Recommended)

هذه الطريقة تستخدم Apache في XAMPP كخادم عكسي (Reverse Proxy) للوصول إلى تطبيق Flask.
This method uses Apache in XAMPP as a reverse proxy to access the Flask application.

#### المزايا:
- سهلة الإعداد
- لا تحتاج تعديلات معقدة في Apache
- Flask يعمل بكامل قدراته
- مناسبة للتطوير والاختبار

#### Advantages:
- Easy setup
- No complex Apache modifications needed
- Flask runs with full capabilities
- Suitable for development and testing

---

### الطريقة 2: استخدام mod_wsgi
### Method 2: Using mod_wsgi

استخدام mod_wsgi لتشغيل Flask مباشرة في Apache.
Using mod_wsgi to run Flask directly in Apache.

#### المزايا:
- أداء أفضل في الإنتاج
- تكامل كامل مع Apache
- إدارة أفضل للموارد

#### Advantages:
- Better production performance
- Full Apache integration
- Better resource management

---

## 🚀 الطريقة 1: تشغيل Flask مع Apache كخادم عكسي

### الخطوة 1: تثبيت المتطلبات

#### 1.1 تثبيت XAMPP
1. قم بتحميل XAMPP من: https://www.apachefriends.org/download.html
2. قم بتثبيت XAMPP (الافتراضي: `C:\xampp` على Windows أو `/opt/lampp` على Linux)
3. تشغيل XAMPP Control Panel

#### 1.2 تثبيت Python
1. قم بتحميل Python 3.11+ من: https://www.python.org/downloads/
2. تأكد من تحديد "Add Python to PATH" أثناء التثبيت
3. تحقق من التثبيت:
```bash
python --version
```

#### 1.3 تثبيت متطلبات المشروع
```bash
# انتقل إلى مجلد المشروع
cd C:\xampp\htdocs\housing-system

# قم بتثبيت المكتبات
pip install -r requirements.txt
```

---

### الخطوة 2: إعداد المشروع

#### 2.1 نسخ ملفات المشروع
```bash
# انسخ مجلد المشروع إلى
# Windows: C:\xampp\htdocs\housing-system
# Linux: /opt/lampp/htdocs/housing-system
```

#### 2.2 إعداد ملف البيئة
أنشئ ملف `.env` في مجلد المشروع:
```env
OPENAI_API_KEY=your-api-key-here
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_PATH=housing_database.db
```

---

### الخطوة 3: إعداد Apache للخادم العكسي

#### 3.1 تفعيل وحدات Apache المطلوبة
افتح ملف `httpd.conf` في XAMPP:
- Windows: `C:\xampp\apache\conf\httpd.conf`
- Linux: `/opt/lampp/etc/httpd.conf`

تأكد من إلغاء التعليق عن السطور التالية (احذف # من البداية):
```apache
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so
LoadModule rewrite_module modules/mod_rewrite.so
```

#### 3.2 إنشاء Virtual Host
أضف التكوين التالي في نهاية ملف `httpd.conf`:

```apache
# نظام إدارة الإسكان الجامعي - Housing Management System
<VirtualHost *:80>
    ServerName housing.local
    ServerAlias www.housing.local
    
    # مجلد المشروع
    DocumentRoot "C:/xampp/htdocs/housing-system"
    
    # إعدادات Proxy
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    
    # السماح بالوصول
    <Directory "C:/xampp/htdocs/housing-system">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    # تسجيل الأخطاء
    ErrorLog "logs/housing-error.log"
    CustomLog "logs/housing-access.log" combined
</VirtualHost>
```

**ملاحظة لمستخدمي Linux:** غيّر المسار إلى:
```apache
DocumentRoot "/opt/lampp/htdocs/housing-system"
<Directory "/opt/lampp/htdocs/housing-system">
```

#### 3.3 تحديث ملف hosts
أضف السطر التالي إلى ملف hosts:
- Windows: `C:\Windows\System32\drivers\etc\hosts`
- Linux: `/etc/hosts`

```
127.0.0.1    housing.local
```

---

### الخطوة 4: تشغيل التطبيق

#### 4.1 تشغيل Flask
افتح نافذة Command Prompt أو Terminal:

```bash
# انتقل إلى مجلد المشروع
cd C:\xampp\htdocs\housing-system

# على Windows
python app.py

# على Linux
python3 app.py
```

يجب أن ترى رسالة مثل:
```
 * Running on http://127.0.0.1:5000
```

#### 4.2 إعادة تشغيل Apache
من XAMPP Control Panel:
1. أوقف Apache
2. شغّل Apache مرة أخرى

---

### الخطوة 5: الوصول إلى التطبيق

افتح المتصفح وانتقل إلى:
```
http://housing.local
```

أو استخدم:
```
http://localhost/housing-system
```

---

## 🔧 الطريقة 2: استخدام mod_wsgi

### المتطلبات الإضافية
```bash
pip install mod_wsgi
```

### إنشاء ملف WSGI
أنشئ ملف `housing.wsgi` في مجلد المشروع:

```python
#!/usr/bin/python
import sys
import os

# مسار المشروع
project_home = '/opt/lampp/htdocs/housing-system'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# تحميل متغيرات البيئة
os.environ['OPENAI_API_KEY'] = 'your-api-key-here'
os.environ['DATABASE_PATH'] = 'housing_database.db'

# استيراد التطبيق
from app import app as application
```

### تكوين Apache
أضف إلى `httpd.conf`:

```apache
WSGIScriptAlias /housing /opt/lampp/htdocs/housing-system/housing.wsgi

<Directory /opt/lampp/htdocs/housing-system>
    WSGIProcessGroup housing
    WSGIApplicationGroup %{GLOBAL}
    Require all granted
</Directory>
```

---

## 🔒 تشغيل Flask كخدمة (للإنتاج)

### على Windows: إنشاء خدمة Windows Service

#### 1. تثبيت NSSM (Non-Sucking Service Manager)
```bash
# قم بتحميل NSSM من: https://nssm.cc/download
# استخرج nssm.exe إلى مجلد
```

#### 2. إنشاء سكريبت بدء التشغيل
أنشئ ملف `start_flask.bat`:

```batch
@echo off
cd /d C:\xampp\htdocs\housing-system
set OPENAI_API_KEY=your-api-key-here
set FLASK_ENV=production
python app.py
```

#### 3. تسجيل الخدمة
```bash
nssm install HousingFlaskService "C:\xampp\htdocs\housing-system\start_flask.bat"
nssm start HousingFlaskService
```

### على Linux: إنشاء Systemd Service

أنشئ ملف `/etc/systemd/system/housing-flask.service`:

```ini
[Unit]
Description=Housing Management Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/lampp/htdocs/housing-system
Environment="OPENAI_API_KEY=your-api-key-here"
Environment="FLASK_ENV=production"
ExecStart=/usr/bin/python3 /opt/lampp/htdocs/housing-system/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

تفعيل وتشغيل الخدمة:
```bash
sudo systemctl daemon-reload
sudo systemctl enable housing-flask
sudo systemctl start housing-flask
sudo systemctl status housing-flask
```

---

## 📦 البديل: استخدام Gunicorn (موصى به للإنتاج)

### التثبيت
```bash
pip install gunicorn
```

### التشغيل
```bash
# تشغيل مع 4 عمال (workers)
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

### إنشاء سكريبت تشغيل
أنشئ ملف `run_gunicorn.sh` (Linux) أو `run_gunicorn.bat` (Windows):

**Linux:**
```bash
#!/bin/bash
cd /opt/lampp/htdocs/housing-system
export OPENAI_API_KEY=your-api-key-here
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

**Windows:**
```batch
@echo off
cd /d C:\xampp\htdocs\housing-system
set OPENAI_API_KEY=your-api-key-here
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

---

## 🐛 حل المشاكل الشائعة

### المشكلة 1: Apache لا يعمل
**الحل:**
- تأكد من إغلاق Skype أو برامج أخرى تستخدم المنفذ 80
- في XAMPP Config، غيّر المنفذ إلى 8080 إذا لزم الأمر

### المشكلة 2: خطأ "Module not found"
**الحل:**
```bash
pip install -r requirements.txt
```

### المشكلة 3: قاعدة البيانات لا تعمل
**الحل:**
- تأكد من وجود ملف `housing_database.db` في مجلد المشروع
- تحقق من صلاحيات الملف

### المشكلة 4: خطأ في OpenAI API
**الحل:**
- تحقق من صحة `OPENAI_API_KEY` في ملف `.env`
- تأكد من توفر رصيد في حساب OpenAI

### المشكلة 5: Proxy Error
**الحل:**
- تأكد من تشغيل Flask على المنفذ 5000
- تحقق من تفعيل mod_proxy في Apache

---

## 📊 اختبار التطبيق

### 1. اختبار الصفحة الرئيسية
افتح: `http://housing.local` أو `http://localhost`

### 2. اختبار API
```bash
curl http://localhost/api/statistics
```

### 3. تسجيل الدخول
- اسم المستخدم: `admin`
- كلمة المرور: `Admin@2025`

---

## 🔐 الأمان في الإنتاج

### 1. استخدم HTTPS
قم بتكوين SSL في XAMPP:
```apache
<VirtualHost *:443>
    ServerName housing.local
    SSLEngine on
    SSLCertificateFile "conf/ssl.crt/server.crt"
    SSLCertificateKeyFile "conf/ssl.key/server.key"
    
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
</VirtualHost>
```

### 2. قيّد الوصول
أضف في Apache config:
```apache
<Directory "C:/xampp/htdocs/housing-system">
    Require ip 192.168.1.0/24  # السماح فقط للشبكة المحلية
</Directory>
```

### 3. احمِ ملف .env
تأكد من عدم إمكانية الوصول إلى ملف `.env` من الويب:
```apache
<Files ".env">
    Require all denied
</Files>
```

---

## 📝 ملاحظات إضافية

### للتطوير
- استخدم الطريقة 1 (Reverse Proxy)
- شغّل Flask في وضع debug: `FLASK_ENV=development`

### للإنتاج
- استخدم Gunicorn مع عدة workers
- فعّل HTTPS
- استخدم قاعدة بيانات أقوى (PostgreSQL/MySQL) بدلاً من SQLite
- نفّذ نسخ احتياطية دورية

### الأداء
- استخدم Gunicorn بدلاً من Flask development server
- فعّل التخزين المؤقت (caching)
- استخدم CDN للملفات الثابتة

---

## 📞 الدعم الفني

إذا واجهت أي مشاكل:
1. راجع سجلات Apache: `logs/housing-error.log`
2. راجع سجلات Flask
3. تأكد من تثبيت جميع المتطلبات
4. تحقق من إعدادات الجدار الناري

---

## 🎓 معلومات المشروع

- **المؤسسة:** جامعة الإمام محمد بن سعود الإسلامية
- **النظام:** نظام إدارة الإسكان الجامعي
- **التقنيات:** Flask, Python, SQLite, OpenAI
- **الترخيص:** للاستخدام الداخلي

---

## 📚 مراجع مفيدة

- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [Apache mod_proxy Guide](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html)
- [XAMPP Documentation](https://www.apachefriends.org/docs/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

تم إنشاء هذا الدليل بواسطة GitHub Copilot
© 2025 جامعة الإمام محمد بن سعود الإسلامية
