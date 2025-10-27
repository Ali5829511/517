# دليل نشر نظام إدارة الإسكان الجامعي

## معلومات المشروع

- **اسم المشروع:** نظام إدارة الإسكان الجامعي
- **التقنيات:** Flask, OpenAI API, Python 3.11
- **الرابط الحالي (يعمل الآن):** https://5000-ig2vo5teusbk2uvgzjffr-6910f30e.manusvm.computer

---

## المتطلبات الأساسية

1. **Python 3.11** أو أحدث
2. **OpenAI API Key** (يجب الحصول عليه من https://platform.openai.com/api-keys)
3. حساب على إحدى منصات الاستضافة التالية:
   - Railway.app
   - Render.com
   - PythonAnywhere
   - Vercel
   - Heroku

---

## طريقة النشر على Railway.app (موصى به)

### الخطوة 1: إنشاء حساب
1. اذهب إلى https://railway.app
2. سجل دخول باستخدام GitHub

### الخطوة 2: إنشاء مشروع جديد
1. انقر على "New Project"
2. اختر "Deploy from GitHub repo"
3. اختر المستودع الذي رفعت فيه المشروع

### الخطوة 3: إعداد متغيرات البيئة
1. في لوحة التحكم، اذهب إلى "Variables"
2. أضف المتغير التالي:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

### الخطوة 4: النشر
- سيتم النشر تلقائياً
- ستحصل على رابط دائم مثل: `https://your-app.railway.app`

---

## طريقة النشر على Render.com

### الخطوة 1: إنشاء حساب
1. اذهب إلى https://render.com
2. سجل دخول باستخدام GitHub

### الخطوة 2: إنشاء Web Service
1. انقر على "New +" ثم "Web Service"
2. اختر المستودع من GitHub
3. املأ البيانات التالية:
   - **Name:** faculty-housing-system
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### الخطوة 3: إعداد متغيرات البيئة
1. في قسم "Environment Variables"
2. أضف:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

### الخطوة 4: النشر
- انقر على "Create Web Service"
- انتظر حتى يكتمل النشر
- ستحصل على رابط مثل: `https://faculty-housing-system.onrender.com`

---

## طريقة النشر على PythonAnywhere

### الخطوة 1: إنشاء حساب
1. اذهب إلى https://www.pythonanywhere.com
2. سجل حساب مجاني

### الخطوة 2: رفع الملفات
1. اذهب إلى "Files"
2. ارفع جميع ملفات المشروع

### الخطوة 3: إنشاء Web App
1. اذهب إلى "Web"
2. انقر على "Add a new web app"
3. اختر "Flask"
4. اختر Python 3.11

### الخطوة 4: تكوين التطبيق
1. في "WSGI configuration file"، عدّل المسار إلى `app.py`
2. في "Virtualenv"، أنشئ بيئة افتراضية:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 housing-env
   pip install -r requirements.txt
   ```

### الخطوة 5: إعداد متغيرات البيئة
1. في "WSGI configuration file"، أضف في البداية:
   ```python
   import os
   os.environ['OPENAI_API_KEY'] = 'your-api-key-here'
   ```

### الخطوة 6: إعادة التحميل
- انقر على "Reload" في صفحة Web
- ستحصل على رابط مثل: `https://username.pythonanywhere.com`

---

## طريقة النشر على Vercel

### الخطوة 1: إنشاء حساب
1. اذهب إلى https://vercel.com
2. سجل دخول باستخدام GitHub

### الخطوة 2: إنشاء ملف vercel.json
أنشئ ملف `vercel.json` في جذر المشروع:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### الخطوة 3: النشر
1. انقر على "New Project"
2. اختر المستودع من GitHub
3. أضف متغير البيئة `OPENAI_API_KEY`
4. انقر على "Deploy"

---

## الحصول على OpenAI API Key

1. اذهب إلى https://platform.openai.com
2. سجل دخول أو أنشئ حساب
3. اذهب إلى "API Keys"
4. انقر على "Create new secret key"
5. انسخ المفتاح واحفظه في مكان آمن

---

## اختبار النظام بعد النشر

1. افتح الرابط الذي حصلت عليه
2. يجب أن تظهر لوحة التحكم الرئيسية
3. جرب رفع صورة لوحة سيارة في صفحة "استخراج اللوحات"
4. تأكد من عمل جميع الميزات

---

## حل المشاكل الشائعة

### المشكلة: خطأ في OpenAI API
**الحل:** تأكد من أن `OPENAI_API_KEY` مضبوط بشكل صحيح في متغيرات البيئة

### المشكلة: الصفحة لا تظهر
**الحل:** تأكد من أن الخادم يعمل على المنفذ الصحيح (عادة 5000 أو 8000)

### المشكلة: خطأ في تثبيت المكتبات
**الحل:** تأكد من أن `requirements.txt` موجود وصحيح

---

## معلومات الاتصال

- **الجامعة:** جامعة الإمام محمد بن سعود الإسلامية
- **البريد الإلكتروني:** housing@imamu.edu.sa
- **الحساب على PythonAnywhere:** imamhousing2025

---

## الرابط الحالي (يعمل الآن)

https://5000-ig2vo5teusbk2uvgzjffr-6910f30e.manusvm.computer

يمكنك استخدام هذا الرابط مباشرة حتى تقوم بنشر المشروع على منصة دائمة.

---

## ملاحظات مهمة

1. **الأمان:** لا تشارك `OPENAI_API_KEY` مع أحد
2. **التكلفة:** استخدام OpenAI API قد يكون له تكلفة، راقب الاستخدام
3. **النسخ الاحتياطي:** احفظ نسخة من المشروع دائماً
4. **التحديثات:** تحقق من تحديثات المكتبات بانتظام

---

تم إنشاء هذا الدليل بواسطة نظام Manus AI
© 2025 جامعة الإمام محمد بن سعود الإسلامية

