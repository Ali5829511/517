# دليل التطوير - Development Guide

## نظام إدارة الإسكان الجامعي

هذا الدليل موجه للمطورين الذين يريدون المساهمة في تطوير المشروع أو تعديله.

---

## 📋 المتطلبات - Requirements

### البرمجيات الأساسية
- **Python 3.11+** (مُختبر على 3.11 و 3.12)
- **pip** (مدير حزم Python)
- **git** (للتحكم بالإصدارات)
- **SQLite3** (مضمن مع Python)

### اختياري للتطوير
- **virtualenv** أو **venv** (بيئة افتراضية)
- **VS Code** أو أي محرر نصوص
- **Postman** أو **curl** (لاختبار APIs)

---

## 🚀 إعداد بيئة التطوير - Development Setup

### 1. استنساخ المستودع
```bash
git clone https://github.com/Ali5829511/517.git
cd 517
```

### 2. إنشاء بيئة افتراضية (موصى به)
```bash
# على Linux/Mac
python3 -m venv venv
source venv/bin/activate

# على Windows
python -m venv venv
venv\Scripts\activate
```

### 3. تثبيت الحزم المطلوبة
```bash
pip install -r requirements.txt
```

### 4. تثبيت أدوات التطوير
```bash
pip install pytest pytest-cov black flake8 pylint
```

### 5. إعداد متغيرات البيئة
```bash
# إنشاء ملف .env
echo "OPENAI_API_KEY=your-api-key-here" > .env
echo "FLASK_ENV=development" >> .env
echo "FLASK_DEBUG=1" >> .env
```

### 6. تشغيل التطبيق في وضع التطوير
```bash
# باستخدام Makefile
make dev

# أو مباشرة
python app.py
```

الآن يمكنك الوصول للتطبيق على: http://localhost:5000

---

## 🔨 أوامر التطوير - Development Commands

### استخدام Makefile

```bash
# تثبيت الحزم
make install

# تشغيل التطبيق في وضع التطوير
make dev

# تشغيل الاختبارات
make test

# تشغيل الاختبارات مع تغطية الكود
make test-cov

# فحص جودة الكود
make lint

# تنسيق الكود
make format

# بناء التطبيق للإنتاج
make build

# تنظيف الملفات المؤقتة
make clean

# عرض جميع الأوامر المتاحة
make help
```

---

## 🧪 الاختبارات - Testing

### تشغيل جميع الاختبارات
```bash
pytest
```

### تشغيل اختبارات محددة
```bash
pytest test_app.py
pytest test_app.py::test_app_exists
```

### قياس تغطية الكود
```bash
pytest --cov=. --cov-report=html
# ثم افتح htmlcov/index.html في المتصفح
```

### إضافة اختبارات جديدة
- أنشئ ملف جديد بصيغة `test_*.py`
- استخدم pytest fixtures للإعداد المشترك
- اتبع نمط الاختبارات الموجودة

---

## 📁 هيكل المشروع - Project Structure

```
517/
├── app.py                      # التطبيق الرئيسي
├── database_api.py             # واجهة قاعدة البيانات
├── generate_database.py        # إنشاء قاعدة البيانات
├── generate_reports.py         # توليد التقارير
├── requirements.txt            # حزم Python المطلوبة
├── Makefile                    # أوامر التطوير والبناء
├── .env.example               # مثال على ملف البيئة
├── housing_database.db         # قاعدة البيانات الرئيسية
├── static/                     # الملفات الثابتة (HTML, CSS, JS)
│   ├── index.html
│   ├── login.html
│   └── ...
├── uploads/                    # الصور المرفوعة
├── processed_images/           # الصور المعالجة
└── test_app.py                # ملف الاختبارات

الملفات التوثيقية:
├── README.md                   # الدليل الرئيسي
├── DEVELOPMENT.md              # دليل التطوير (هذا الملف)
├── DEPLOYMENT_GUIDE.md         # دليل النشر
├── QUICK_START.md              # دليل البدء السريع
├── PROJECT_STATUS.md           # حالة المشروع
└── FEATURES_IMPLEMENTATION.md  # تفاصيل الميزات
```

---

## 🔧 التطوير - Development Workflow

### 1. إنشاء فرع جديد
```bash
git checkout -b feature/feature-name
```

### 2. إجراء التعديلات
- عدّل الكود حسب الحاجة
- اختبر التعديلات باستمرار
- تأكد من جودة الكود

### 3. تشغيل الاختبارات
```bash
make test
make lint
```

### 4. حفظ التغييرات
```bash
git add .
git commit -m "وصف واضح للتغييرات"
```

### 5. رفع التغييرات
```bash
git push origin feature/feature-name
```

### 6. إنشاء Pull Request
- اذهب إلى GitHub
- أنشئ Pull Request من فرعك
- أضف وصفاً واضحاً للتغييرات

---

## 🎨 معايير البرمجة - Coding Standards

### Python Style Guide
- اتبع **PEP 8** لتنسيق الكود
- استخدم **Black** للتنسيق التلقائي: `make format`
- استخدم **Flake8** للفحص: `make lint`
- أقصى طول للسطر: 100 حرف

### التسميات
- **الفئات (Classes):** `CamelCase`
- **الدوال (Functions):** `snake_case`
- **الثوابت (Constants):** `UPPER_SNAKE_CASE`
- **المتغيرات (Variables):** `snake_case`

### التعليقات والتوثيق
- استخدم docstrings للدوال والفئات
- علّق على الكود المعقد فقط
- استخدم العربية أو الإنجليزية بثبات

### مثال على دالة موثقة:
```python
def calculate_parking_fee(hours, rate=10):
    """
    حساب رسوم موقف السيارات
    
    Args:
        hours (int): عدد الساعات
        rate (int): السعر لكل ساعة (افتراضي: 10)
    
    Returns:
        int: إجمالي الرسوم
    """
    return hours * rate
```

---

## 🐛 تصحيح الأخطاء - Debugging

### تفعيل وضع Debug
```bash
export FLASK_DEBUG=1
python app.py
```

### استخدام Python Debugger
```python
import pdb; pdb.set_trace()
```

### فحص السجلات (Logs)
```bash
# عرض آخر 50 سطر من السجلات
tail -f -n 50 app.log
```

---

## 🔒 الأمان - Security

### أفضل الممارسات
1. **لا تضف مفاتيح API** إلى Git
2. استخدم **متغيرات البيئة** للبيانات الحساسة
3. **لا تعطل CSRF protection** في الإنتاج
4. استخدم **HTTPS** في الإنتاج
5. **نظّف المدخلات** من المستخدمين

### فحص الثغرات الأمنية
```bash
pip install safety
safety check
```

---

## 📊 قاعدة البيانات - Database

### هيكل قاعدة البيانات
- **residents:** بيانات السكان
- **buildings:** بيانات المباني
- **residential_units:** الوحدات السكنية
- **stickers:** ملصقات السيارات
- **parking_spots:** مواقف السيارات

### إعادة إنشاء قاعدة البيانات
```bash
python generate_database.py
```

### فحص قاعدة البيانات
```bash
sqlite3 housing_database.db
sqlite> .tables
sqlite> SELECT COUNT(*) FROM residents;
sqlite> .quit
```

### نسخة احتياطية
```bash
cp housing_database.db housing_database.backup.db
```

---

## 🔄 API Endpoints

### قائمة APIs المتاحة

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | الصفحة الرئيسية |
| `/login` | GET, POST | تسجيل الدخول |
| `/api/residents` | GET | قائمة السكان |
| `/api/buildings` | GET | قائمة المباني |
| `/api/stickers` | GET | قائمة الملصقات |
| `/api/parking` | GET | قائمة المواقف |
| `/api/statistics` | GET | إحصائيات عامة |
| `/api/search` | POST | البحث في النظام |

### اختبار APIs
```bash
# استخدام curl
curl http://localhost:5000/api/statistics

# استخدام httpie (أفضل)
pip install httpie
http GET http://localhost:5000/api/statistics
```

---

## 🚢 الإنتاج - Production

### بناء للإنتاج
```bash
make build
```

### اختبار الإنتاج محلياً
```bash
gunicorn app:app --bind 0.0.0.0:8000
```

### النشر
راجع ملف `DEPLOYMENT_GUIDE.md` للتفاصيل الكاملة

---

## 📚 الموارد - Resources

### التوثيق الرسمي
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python Documentation](https://docs.python.org/3/)

### أدوات مفيدة
- [Postman](https://www.postman.com/) - اختبار APIs
- [DB Browser for SQLite](https://sqlitebrowser.org/) - عرض قاعدة البيانات
- [VS Code](https://code.visualstudio.com/) - محرر الكود

---

## 🆘 الدعم والمساعدة

### الإبلاغ عن مشكلة
1. افتح issue على GitHub
2. صف المشكلة بوضوح
3. أرفق لقطة شاشة إن أمكن
4. اذكر خطوات إعادة إنتاج المشكلة

### الاتصال
- **GitHub Issues:** https://github.com/Ali5829511/517/issues
- **Email:** housing@imamu.edu.sa

---

## 📝 الملاحظات

- هذا مشروع تعليمي/إنتاجي لجامعة الإمام
- البيانات في قاعدة البيانات عينة للتطوير
- في الإنتاج، استخدم بيانات حقيقية
- حافظ على نسخ احتياطية دورية

---

**جامعة الإمام محمد بن سعود الإسلامية**  
**نظام إدارة الإسكان الجامعي**  
**Development Guide v1.0**
