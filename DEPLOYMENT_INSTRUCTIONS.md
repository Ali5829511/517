# تعليمات نشر نظام إدارة الإسكان على Render.com

## الخطوة 1: إنشاء حساب على Render.com

1. اذهب إلى [https://render.com](https://render.com)
2. اضغط على "Get Started" أو "Sign Up"
3. سجل باستخدام GitHub أو البريد الإلكتروني

## الخطوة 2: رفع المشروع إلى GitHub

### الطريقة الأولى: استخدام GitHub Desktop
1. حمّل [GitHub Desktop](https://desktop.github.com)
2. افتح البرنامج واضغط "File" → "Add Local Repository"
3. اختر مجلد المشروع
4. اضغط "Publish repository"
5. سمّه `housing-management-system`
6. اضغط "Publish"

### الطريقة الثانية: استخدام سطر الأوامر
```bash
# في مجلد المشروع
git remote add origin https://github.com/YOUR_USERNAME/housing-management-system.git
git branch -M main
git push -u origin main
```

## الخطوة 3: النشر على Render.com

1. سجل الدخول إلى [Render.com](https://dashboard.render.com)
2. اضغط "New +" → "Web Service"
3. اختر "Build and deploy from a Git repository"
4. اربط حساب GitHub إذا لم يكن مربوطاً
5. اختر المستودع `housing-management-system`
6. املأ البيانات:
   - **Name:** `housing-management-system`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** `Free`
7. اضغط "Create Web Service"

## الخطوة 4: انتظر اكتمال النشر

- سيستغرق النشر من 3-5 دقائق
- ستحصل على رابط مثل: `https://housing-management-system.onrender.com`

## الروابط المهمة بعد النشر

- البوابة الرئيسية: `https://your-app.onrender.com/main_portal.html`
- لوحة المعلومات: `https://your-app.onrender.com/interactive_dashboard.html`
- التقارير الشاملة: `https://your-app.onrender.com/comprehensive_reports.html`
- النظام الرئيسي: `https://your-app.onrender.com/index.html`

## ملاحظات مهمة

### الخطة المجانية
- ✅ مجانية تماماً
- ✅ HTTPS تلقائي
- ✅ 750 ساعة شهرياً
- ⚠️ يتوقف بعد 15 دقيقة من عدم النشاط (يعود تلقائياً عند الزيارة)

### الترقية للخطة المدفوعة (اختياري)
- $7/شهر
- يعمل 24/7 بدون توقف
- أسرع وأكثر استقراراً

## استكشاف الأخطاء

### إذا فشل النشر:
1. تحقق من ملف `requirements.txt`
2. تحقق من أن `gunicorn` موجود في requirements.txt
3. راجع سجلات الأخطاء في Render Dashboard

### إذا لم تظهر البيانات:
- تأكد من وجود ملف `housing_database.db` في المشروع
- تحقق من APIs في `/api/residents`, `/api/buildings`, إلخ

## الدعم الفني

للمساعدة:
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)

---

**جامعة الإمام محمد بن سعود الإسلامية**  
**نظام إدارة الإسكان**
