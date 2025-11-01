# قائمة التحقق من إعداد XAMPP
# XAMPP Setup Checklist

استخدم هذه القائمة للتأكد من إكمال جميع خطوات التثبيت بنجاح.
Use this checklist to ensure all installation steps are completed successfully.

---

## ✅ المتطلبات الأساسية - Prerequisites

### 1. تثبيت XAMPP
- [ ] تم تحميل XAMPP من https://www.apachefriends.org/download.html
- [ ] تم تثبيت XAMPP في المسار:
  - Windows: `C:\xampp`
  - Linux: `/opt/lampp`
- [ ] يمكن فتح XAMPP Control Panel
- [ ] Apache يعمل بدون أخطاء
- [ ] MySQL يعمل (اختياري - غير مطلوب للمشروع)

### 2. تثبيت Python
- [ ] تم تحميل Python 3.11+ من https://www.python.org/downloads/
- [ ] تم تحديد "Add Python to PATH" أثناء التثبيت
- [ ] يعمل الأمر: `python --version` أو `python3 --version`
- [ ] يعمل الأمر: `pip --version`

### 3. الحصول على OpenAI API Key
- [ ] تم إنشاء حساب على https://platform.openai.com
- [ ] تم الحصول على API Key من https://platform.openai.com/api-keys
- [ ] تم نسخ وحفظ API Key في مكان آمن

---

## 📁 إعداد المشروع - Project Setup

### 1. نسخ الملفات
- [ ] تم نسخ مجلد المشروع إلى:
  - Windows: `C:\xampp\htdocs\housing-system`
  - Linux: `/opt/lampp/htdocs/housing-system`
- [ ] جميع الملفات موجودة:
  - [ ] `app.py`
  - [ ] `requirements.txt`
  - [ ] `housing_database.db`
  - [ ] مجلد `static/`
  - [ ] سكريبتات البدء (`start_flask_*.bat` / `.sh`)

### 2. تثبيت المكتبات
- [ ] تم فتح Command Prompt / Terminal
- [ ] تم الانتقال إلى مجلد المشروع
- [ ] تم تنفيذ: `pip install -r requirements.txt`
- [ ] تم التثبيت بدون أخطاء
- [ ] تم التحقق من التثبيت: `pip list | grep Flask`

### 3. إعداد ملف البيئة (.env)
- [ ] تم إنشاء ملف `.env` في مجلد المشروع
- [ ] تم إضافة المتغيرات التالية:
  ```env
  OPENAI_API_KEY=your-actual-api-key
  FLASK_ENV=production
  SECRET_KEY=your-secret-key-change-this
  DATABASE_PATH=housing_database.db
  HOST=127.0.0.1
  PORT=5000
  ```
- [ ] تم التأكد من صحة OPENAI_API_KEY
- [ ] تم تغيير SECRET_KEY إلى قيمة فريدة

---

## 🚀 الطريقة 1: تشغيل مباشر - Direct Run

### 1. اختبار التشغيل المباشر
- [ ] تم فتح Command Prompt / Terminal
- [ ] تم الانتقال إلى مجلد المشروع
- [ ] تم تنفيذ:
  - Windows: `start_flask_windows.bat`
  - Linux: `./start_flask_linux.sh`
- [ ] ظهرت رسالة: `Running on http://127.0.0.1:5000`
- [ ] لا توجد أخطاء في Console

### 2. اختبار الوصول
- [ ] تم فتح المتصفح
- [ ] تم الانتقال إلى: `http://127.0.0.1:5000`
- [ ] ظهرت الصفحة الرئيسية للنظام
- [ ] لا توجد أخطاء 404 أو 500

### 3. اختبار تسجيل الدخول
- [ ] تم الانتقال إلى صفحة تسجيل الدخول
- [ ] تم استخدام:
  - اسم المستخدم: `admin`
  - كلمة المرور: `Admin@2025`
- [ ] تم تسجيل الدخول بنجاح
- [ ] ظهرت لوحة التحكم

---

## 🌐 الطريقة 2: مع Apache (اختياري) - With Apache

### 1. تفعيل وحدات Apache
- [ ] تم فتح ملف `httpd.conf`:
  - Windows: `C:\xampp\apache\conf\httpd.conf`
  - Linux: `/opt/lampp/etc/httpd.conf`
- [ ] تم إلغاء التعليق عن (حذف # من):
  - [ ] `LoadModule proxy_module modules/mod_proxy.so`
  - [ ] `LoadModule proxy_http_module modules/mod_proxy_http.so`
  - [ ] `LoadModule rewrite_module modules/mod_rewrite.so`
  - [ ] `LoadModule headers_module modules/mod_headers.so`

### 2. إضافة Virtual Host
- [ ] تم نسخ محتوى `apache_vhost_config.conf`
- [ ] تم إضافة التكوين إلى نهاية `httpd.conf`
- [ ] تم تعديل المسارات لتطابق التثبيت الفعلي
- [ ] تم حفظ الملف

### 3. تحديث ملف hosts
- [ ] تم فتح ملف hosts:
  - Windows: `C:\Windows\System32\drivers\etc\hosts`
  - Linux: `/etc/hosts`
- [ ] تم إضافة السطر: `127.0.0.1    housing.local`
- [ ] تم حفظ الملف (قد يحتاج صلاحيات مدير)

### 4. إعادة تشغيل Apache
- [ ] من XAMPP Control Panel:
  - [ ] تم إيقاف Apache (Stop)
  - [ ] تم تشغيل Apache (Start)
- [ ] لا توجد أخطاء في سجلات Apache
- [ ] Apache يعمل بشكل طبيعي

### 5. اختبار مع Apache
- [ ] تم تشغيل Flask (باستخدام السكريبت)
- [ ] تم فتح المتصفح
- [ ] تم الانتقال إلى: `http://housing.local`
- [ ] ظهر النظام بنجاح

---

## 🔥 الطريقة 3: مع Gunicorn (موصى به للإنتاج)

### 1. تثبيت Gunicorn
- [ ] تم التأكد من تثبيت Gunicorn: `pip show gunicorn`
- [ ] إذا لم يكن مثبتاً: `pip install gunicorn`

### 2. اختبار Gunicorn
- [ ] تم تنفيذ:
  - Windows: `start_gunicorn_windows.bat`
  - Linux: `./start_gunicorn_linux.sh`
- [ ] ظهرت رسائل Gunicorn بدون أخطاء
- [ ] تم التأكد من عمل 4 workers

### 3. الوصول عبر Gunicorn
- [ ] تم فتح المتصفح
- [ ] تم الانتقال إلى: `http://127.0.0.1:5000`
- [ ] النظام يعمل بشكل صحيح
- [ ] السرعة أفضل من Flask development server

---

## 🧪 الاختبارات الوظيفية - Functional Tests

### 1. اختبار الصفحة الرئيسية
- [ ] يتم تحميل الصفحة الرئيسية
- [ ] القوائم تظهر بشكل صحيح
- [ ] الروابط تعمل

### 2. اختبار قاعدة البيانات
- [ ] صفحة السكان تعرض البيانات
- [ ] صفحة المباني تعرض البيانات
- [ ] صفحة الوحدات السكنية تعرض البيانات
- [ ] صفحة ملصقات السيارات تعرض البيانات

### 3. اختبار API
- [ ] `/api/statistics` يعمل
- [ ] يتم عرض JSON صحيح
- [ ] الإحصائيات صحيحة:
  - [ ] 165 مبنى
  - [ ] 1,134 وحدة سكنية
  - [ ] 1,057 ساكن

### 4. اختبار رفع الصور (إذا كان OpenAI متاح)
- [ ] صفحة استخراج اللوحات تعمل
- [ ] يمكن رفع صورة
- [ ] يتم معالجة الصورة
- [ ] تظهر النتيجة

### 5. اختبار التقارير
- [ ] صفحة التقارير تفتح
- [ ] الرسوم البيانية تظهر
- [ ] يمكن طباعة التقرير
- [ ] يمكن تصدير PDF

---

## 🔐 الأمان - Security

### 1. الملفات المحمية
- [ ] لا يمكن الوصول إلى `.env` من المتصفح
- [ ] لا يمكن الوصول إلى ملفات `.py` مباشرة
- [ ] لا يمكن الوصول إلى قاعدة البيانات `.db` مباشرة
- [ ] لا يظهر directory listing عند الوصول للمجلدات

### 2. تأمين الإنتاج (إذا كان للاستخدام الحقيقي)
- [ ] تم تغيير SECRET_KEY إلى قيمة عشوائية قوية
- [ ] تم تغيير كلمة مرور admin الافتراضية
- [ ] تم تفعيل HTTPS (إذا كان متاحاً)
- [ ] تم تقييد الوصول من IP معين (إذا لزم الأمر)

---

## 📊 الأداء - Performance

### 1. سرعة التحميل
- [ ] الصفحة الرئيسية تحمل في أقل من 3 ثوان
- [ ] صفحات البيانات تحمل بسرعة معقولة
- [ ] الصور تظهر بدون تأخير

### 2. استخدام الموارد
- [ ] استخدام CPU معتدل (أقل من 50%)
- [ ] استخدام RAM معتدل (أقل من 500 MB)
- [ ] لا توجد رسائل خطأ في logs

---

## 🐛 حل المشاكل - Troubleshooting

إذا واجهت مشاكل، تحقق من:

### Python لا يعمل
- [ ] تم تثبيت Python بشكل صحيح
- [ ] Python موجود في PATH
- [ ] يعمل الأمر: `python --version`

### Port 5000 مستخدم
- [ ] لا يوجد برنامج آخر يستخدم المنفذ 5000
- [ ] أو غيّر PORT في ملف `.env` إلى 8000

### Apache لا يعمل
- [ ] لا يوجد Skype أو برنامج آخر يستخدم المنفذ 80
- [ ] تم تفعيل وحدات Proxy في Apache
- [ ] لا توجد أخطاء في `logs/error.log`

### قاعدة البيانات لا تعمل
- [ ] ملف `housing_database.db` موجود
- [ ] للملف صلاحيات القراءة والكتابة
- [ ] المسار صحيح في DATABASE_PATH

### OpenAI لا يعمل
- [ ] OPENAI_API_KEY صحيح في ملف `.env`
- [ ] يوجد رصيد في حساب OpenAI
- [ ] الاتصال بالإنترنت يعمل

---

## 📝 الخطوات التالية - Next Steps

### للاستخدام اليومي:
- [ ] إنشاء shortcut لسكريبت البدء
- [ ] حفظ رابط النظام في المفضلة
- [ ] طباعة معلومات تسجيل الدخول

### للإنتاج:
- [ ] إعداد نسخ احتياطية دورية لقاعدة البيانات
- [ ] مراقبة السجلات (logs) بانتظام
- [ ] تحديث المكتبات بانتظام: `pip install --upgrade -r requirements.txt`

### للتطوير:
- [ ] إنشاء بيئة تطوير منفصلة
- [ ] استخدام `FLASK_ENV=development` للتطوير
- [ ] إعداد Git للتحكم في الإصدارات

---

## ✅ التحقق النهائي - Final Verification

- [ ] ✅ النظام يعمل بدون أخطاء
- [ ] ✅ يمكن تسجيل الدخول
- [ ] ✅ البيانات تظهر بشكل صحيح
- [ ] ✅ جميع الصفحات تعمل
- [ ] ✅ API يستجيب
- [ ] ✅ الأمان مطبق بشكل صحيح

---

## 📞 الحصول على المساعدة

إذا واجهت مشاكل:
1. راجع `XAMPP_DEPLOYMENT.md` للتفاصيل الكاملة
2. تحقق من السجلات في مجلد `logs/`
3. راجع قسم حل المشاكل في `XAMPP_QUICK_START.md`
4. تأكد من اتباع جميع الخطوات في هذه القائمة

---

## 🎓 معلومات المشروع

- **المؤسسة:** جامعة الإمام محمد بن سعود الإسلامية
- **النظام:** نظام إدارة الإسكان الجامعي
- **الإصدار:** 1.0
- **تاريخ التحديث:** نوفمبر 2025

---

**تهانينا! إذا أكملت جميع الخطوات بنجاح، فإن النظام جاهز للاستخدام! 🎉**
**Congratulations! If you've completed all steps successfully, the system is ready to use! 🎉**

---

© 2025 جامعة الإمام محمد بن سعود الإسلامية
تم إنشاء هذا الملف بواسطة GitHub Copilot
