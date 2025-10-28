# خطوات النشر السريع على Render.com

## الإعدادات المطلوبة في صفحة New Web Service

### 1. Source Code
✅ تم اختيار المستودع: `Ali5829511/517`

### 2. Name
```
housing-management-system
```

### 3. Language
اختر: **Python 3**

### 4. Branch
```
main
```

### 5. Build Command
```bash
pip install -r requirements.txt
```

### 6. Start Command
```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

### 7. Instance Type
- **Free** ($0/month) - للتجربة
- **Starter** ($7/month) - للاستخدام الفعلي

### 8. Deploy
اضغط على زر **"Deploy web service"**

---

## الروابط بعد النشر

البوابة الرئيسية:
```
https://housing-management-system.onrender.com/main_portal.html
```

لوحة المعلومات التفاعلية:
```
https://housing-management-system.onrender.com/interactive_dashboard.html
```

---

**ملاحظة:** الخطة المجانية تتوقف بعد 15 دقيقة من عدم النشاط
