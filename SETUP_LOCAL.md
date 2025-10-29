# 🚀 إرشادات التشغيل المحلي / Local Development Setup

## نظرة عامة
تم تحديث التطبيق ليشمل ميزات أمان محسّنة ودعم متغيرات البيئة باستخدام python-dotenv.

## المتطلبات الأساسية
- Python 3.11 أو أحدث
- pip (مدير حزم Python)

## خطوات التثبيت

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. إعداد ملف البيئة
انسخ ملف `.env.example` إلى `.env`:
```bash
cp .env.example .env
```

قم بتحرير ملف `.env` وأضف مفتاح OpenAI API الخاص بك:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
PORT=5000
```

**ملاحظة**: 
- إذا تركت `OPENAI_API_KEY` فارغاً، سيعمل التطبيق في وضع محدود بدون ميزات الذكاء الاصطناعي
- احصل على مفتاح API من: https://platform.openai.com/api-keys

### 3. تشغيل التطبيق
```bash
python app.py
```

سيعمل التطبيق على: http://localhost:5000

## ميزات الأمان الجديدة

### 1. إدارة ملفات التحميل الآمنة
- جميع الملفات المرفوعة تُحفظ بشكل آمن باستخدام `secure_filename`
- يتم حفظ الملفات في مجلد `uploads/` (مستثنى من git)
- الصور المعالجة تُحفظ في `processed_images/` (مستثنى من git)

### 2. إعدادات أمان الجلسة
- `SESSION_COOKIE_SECURE=True`: الكوكيز تُرسل فقط عبر HTTPS
- `SESSION_COOKIE_HTTPONLY=True`: الكوكيز لا يمكن الوصول إليها عبر JavaScript
- `SESSION_COOKIE_SAMESITE='Lax'`: حماية من هجمات CSRF

### 3. نظام التسجيل (Logging)
- استبدال جميع `print()` بـ `logger` المناسب
- تسجيل الأخطاء والتحذيرات بشكل منظم
- مستوى التسجيل الافتراضي: INFO

### 4. تهيئة OpenAI الآمنة
- تحميل مفتاح API من متغيرات البيئة
- معالجة الأخطاء المحسّنة
- إرجاع رمز حالة 503 عند عدم توفر الخدمة

## اختبار التطبيق

### تشغيل الاختبارات
```bash
# تشغيل جميع الاختبارات
pytest

# تشغيل اختبارات محددة
pytest test_app.py -v
pytest test_security_features.py -v
pytest test_secure_upload.py -v
```

### الاختبارات المتوفرة
- **test_app.py**: اختبارات أساسية للتطبيق (4 اختبارات)
- **test_security_features.py**: اختبارات ميزات الأمان (8 اختبارات)
- **test_secure_upload.py**: اختبارات تحميل الملفات الآمن (5 اختبارات)

## وضع Mock (بدون OpenAI)

إذا لم يكن لديك مفتاح OpenAI API، يمكنك اختبار التطبيق في وضع محدود:

1. احذف أو اترك `OPENAI_API_KEY` فارغاً في ملف `.env`
2. شغّل التطبيق - سيعمل بدون ميزات الذكاء الاصطناعي
3. الوظائف التي تعتمد على OpenAI ستُرجع رمز حالة 503

## استكشاف الأخطاء

### خطأ: ModuleNotFoundError
```bash
# تأكد من تثبيت جميع المتطلبات
pip install -r requirements.txt
```

### خطأ: OPENAI_API_KEY not found
```bash
# تأكد من وجود ملف .env في المجلد الحالي
# وأنه يحتوي على OPENAI_API_KEY
cat .env
```

### مشاكل الصلاحيات
```bash
# تأكد من أن مجلدات التحميل قابلة للكتابة
chmod 755 uploads/
chmod 755 processed_images/
```

## البنية الأساسية للملفات

```
.
├── app.py                      # التطبيق الرئيسي
├── requirements.txt            # متطلبات Python
├── .env.example               # مثال لملف البيئة
├── .env                       # ملف البيئة الفعلي (لا يُرفع لـ git)
├── .gitignore                 # ملفات مستثناة من git
├── uploads/                   # مجلد الملفات المرفوعة
├── processed_images/          # مجلد الصور المعالجة
├── static/                    # ملفات HTML/CSS/JS
├── test_app.py                # اختبارات أساسية
├── test_security_features.py  # اختبارات الأمان
└── test_secure_upload.py      # اختبارات التحميل الآمن
```

## ملاحظات مهمة

1. **لا تشارك ملف .env**: يحتوي على بيانات حساسة
2. **استخدم .env.example كمرجع**: للمطورين الجدد
3. **HTTPS في الإنتاج**: تأكد من استخدام HTTPS في بيئة الإنتاج لتفعيل SESSION_COOKIE_SECURE
4. **نسخ احتياطي لقاعدة البيانات**: احفظ نسخ احتياطية منتظمة من housing_database.db

## الدعم والمساعدة

إذا واجهت أي مشاكل:
1. تحقق من السجلات (logs)
2. راجع التوثيق في المستودع
3. افتح issue في GitHub
