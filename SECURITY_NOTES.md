# ملاحظات الأمان - Security Notes

## 🔐 نقاط أمنية مهمة - Important Security Points

### 1. كلمة المرور الافتراضية ⚠️
**المشكلة:**
- يحتوي الكود على مستخدم افتراضي بكلمة مرور ثابتة
- الموقع: `app.py` السطر 85-92

**الحل الموصى به:**
```python
# في app.py، غيّر هذا:
users_db = {
    "admin": {
        "password": generate_password_hash("Admin@2025"),  # ⚠️ غير هذا!
        "role": "admin",
        "name": "مدير النظام",
        "email": "admin@example.com",  # ⚠️ غير هذا أيضاً!
    }
}

# إلى كلمة مرور قوية:
users_db = {
    "admin": {
        "password": generate_password_hash("YourSecurePassword123!@#"),
        "role": "admin",
        "name": "مدير النظام",
        "email": "your-email@yourdomain.com",
    }
}
```

**أو استخدم متغيرات البيئة:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

users_db = {
    "admin": {
        "password": generate_password_hash(os.getenv("ADMIN_PASSWORD", "TempPassword123!")),
        "role": "admin",
        "name": "مدير النظام",
        "email": os.getenv("ADMIN_EMAIL", "admin@example.com"),
    }
}
```

ثم في ملف `.env`:
```
ADMIN_PASSWORD=YourVerySecurePassword123!@#
ADMIN_EMAIL=your-email@yourdomain.com
```

---

### 2. المفتاح السري - SECRET_KEY

**الحالة الحالية:**
المفتاح السري موجود في `config.py` ويجب تغييره في الإنتاج.

**الموقع:** `config.py` السطر ~20

**الحل:**
```python
# في config.py
class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-very-long-random-secret-key-here'
```

**إنشاء مفتاح عشوائي قوي:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

### 3. قاعدة البيانات الافتراضية

**الحالة الحالية:**
- قاعدة البيانات `housing_database.db` مرفوعة في Git
- تحتوي على بيانات تجريبية

**للإنتاج:**
1. أنشئ قاعدة بيانات جديدة فارغة
2. لا ترفع قاعدة البيانات مع الكود
3. استخدم backup منفصل لقاعدة البيانات

**إضافة لـ .gitignore:**
```
# في الإنتاج، أضف:
*.db
!schema.db  # احتفظ بملف المخطط فقط
```

---

### 4. مفتاح OpenAI API

**الحالة الحالية:**
النظام يبحث عن `OPENAI_API_KEY` في متغيرات البيئة

**الأمان:**
✅ لا يتم تخزين المفتاح في الكود (ممتاز!)
✅ النظام يعمل بدون المفتاح (fallback جيد)

**للإنتاج:**
```bash
# لا تضع المفتاح في الكود أبداً!
# استخدم متغيرات البيئة:
export OPENAI_API_KEY="sk-your-actual-key-here"

# أو في ملف .env (لا ترفعه لـ Git!)
OPENAI_API_KEY=sk-your-actual-key-here
```

---

### 5. الجلسات - Sessions

**الحالة الحالية:**
✅ الجلسات محمية بشكل جيد
✅ يستخدم SECRET_KEY للتشفير
✅ HttpOnly و SameSite محددة

**تحسينات إضافية:**
```python
# في app.py، أضف:
app.config['SESSION_COOKIE_SECURE'] = True  # للـ HTTPS فقط
app.config['SESSION_COOKIE_HTTPONLY'] = True  # يمنع JavaScript من الوصول
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # حماية CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # انتهاء الجلسة
```

---

### 6. تحميل الملفات - File Uploads

**الحالة الحالية:**
✅ يتم التحقق من امتدادات الملفات
✅ حجم الملفات محدود (16 MB)

**تحسينات موصى بها:**
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB أفضل من 16 MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# تحقق من نوع الملف الفعلي وليس الامتداد فقط
from PIL import Image

def verify_image(file_path):
    try:
        img = Image.open(file_path)
        img.verify()
        return True
    except:
        return False
```

---

### 7. حقن SQL - SQL Injection

**الحالة الحالية:**
✅ يستخدم parameterized queries في معظم الأماكن
✅ لا توجد مشاكل SQL injection واضحة

**التأكد:**
```python
# جيد ✅
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

# سيء ❌ (لا تستخدم أبداً!)
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

---

### 8. Cross-Site Scripting (XSS)

**الحالة الحالية:**
✅ Flask يستخدم Jinja2 الذي ينظف الإدخال تلقائياً
✅ jsonify() يستخدم في الـ API

**للتأكد:**
- لا تستخدم `|safe` في Jinja2 إلا للمحتوى الموثوق
- نظف البيانات قبل عرضها في HTML

---

### 9. Rate Limiting (حد المحاولات)

**الحالة الحالية:**
⚠️ لا يوجد rate limiting حالياً

**التحسين الموصى به:**
```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")  # 5 محاولات فقط في الدقيقة
def login():
    # ...
```

---

### 10. HTTPS في الإنتاج

**مهم جداً:**
- استخدم HTTPS دائماً في الإنتاج
- معظم منصات النشر (Railway, Render) توفر HTTPS تلقائياً
- للـ XAMPP المحلي، HTTPS اختياري

**للتحقق:**
```python
# في config.py
class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True  # يفرض HTTPS
    PREFERRED_URL_SCHEME = 'https'
```

---

## ✅ قائمة التحقق الأمني - Security Checklist

قبل النشر في الإنتاج، تأكد من:

- [ ] تغيير كلمة المرور الافتراضية
- [ ] تغيير SECRET_KEY إلى قيمة عشوائية قوية
- [ ] إضافة OPENAI_API_KEY في متغيرات البيئة (إذا لزم)
- [ ] عدم رفع ملف .env إلى Git
- [ ] تفعيل HTTPS
- [ ] تحديد SESSION_COOKIE_SECURE = True
- [ ] إضافة Rate Limiting لصفحة تسجيل الدخول
- [ ] مراجعة صلاحيات الملفات على الخادم
- [ ] إعداد نسخ احتياطي تلقائي لقاعدة البيانات
- [ ] مراقبة logs للأخطاء والهجمات
- [ ] تحديث الحزم بانتظام (`pip list --outdated`)
- [ ] فحص الثغرات الأمنية (`safety check`)

---

## 🛡️ الأدوات الأمنية الموصى بها

### فحص الثغرات
```bash
# تثبيت أدوات الفحص
pip install safety bandit

# فحص الحزم
safety check

# فحص الكود
bandit -r . -ll
```

### مراقبة الأمان
```bash
# فحص شامل
make security  # (إذا كان موجوداً في Makefile)
```

---

## 📞 الإبلاغ عن مشاكل أمنية

إذا اكتشفت ثغرة أمنية:
1. **لا تنشرها علناً**
2. راسل مطور المشروع مباشرة
3. قدم تفاصيل دقيقة عن الثغرة
4. انتظر حتى يتم الإصلاح قبل النشر

---

**آخر تحديث:** 4 نوفمبر 2025  
**المشروع:** نظام إدارة الإسكان الجامعي

⚠️ **تنبيه:** هذا المستند يحتوي على معلومات أمنية حساسة. لا تشاركه علناً.
