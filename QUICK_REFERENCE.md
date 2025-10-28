# مرجع سريع - Quick Reference

## نظام إدارة الإسكان الجامعي

---

## ⚡ أوامر سريعة - Quick Commands

### الإعداد:
```bash
./setup_dev.sh              # إعداد بيئة التطوير
source venv/bin/activate    # تفعيل البيئة الافتراضية
```

### التشغيل:
```bash
make dev                    # تشغيل في وضع التطوير
make run                    # تشغيل عادي
make run-prod               # تشغيل للإنتاج
```

### الاختبار:
```bash
make test                   # تشغيل الاختبارات
make test-cov               # اختبار مع التغطية
make check                  # فحص شامل
```

### الجودة:
```bash
make lint                   # فحص جودة الكود
make format                 # تنسيق الكود
make security               # فحص أمني
```

### البناء:
```bash
make build                  # بناء للإنتاج
./build.sh                  # بناء بسكريبت
make clean                  # تنظيف
```

### قاعدة البيانات:
```bash
make db-init                # إنشاء قاعدة البيانات
make db-inspect             # فحص البيانات
make db-backup              # نسخة احتياطية
```

### معلومات:
```bash
make help                   # عرض المساعدة
make status                 # حالة المشروع
make info                   # معلومات البيئة
```

---

## 📁 هيكل المشروع - Project Structure

```
517/
├── app.py                  # التطبيق الرئيسي
├── config.py               # إعدادات التكوين
├── database_api.py         # واجهة قاعدة البيانات
├── Makefile                # أوامر التطوير
├── setup_dev.sh            # سكريبت الإعداد
├── build.sh                # سكريبت البناء
├── requirements.txt        # الحزم المطلوبة
├── .env.example           # مثال ملف البيئة
├── .gitignore              # ملفات مستثناة
├── housing_database.db     # قاعدة البيانات
├── static/                 # ملفات HTML/CSS/JS
├── test_*.py               # ملفات الاختبار
└── docs/
    ├── README.md           # نظرة عامة
    ├── DEVELOPMENT.md      # دليل التطوير
    ├── WORKFLOW.md         # سير العمل
    ├── QUICK_START.md      # بدء سريع
    └── DEPLOYMENT_GUIDE.md # دليل النشر
```

---

## 🔧 ملف .env

```bash
FLASK_ENV=development
FLASK_DEBUG=1
OPENAI_API_KEY=sk-your-key-here
DATABASE_PATH=housing_database.db
UPLOAD_FOLDER=uploads
PROCESSED_FOLDER=processed_images
```

---

## 🌐 URLs مهمة

### محلي:
- **التطبيق:** http://localhost:5000
- **API:** http://localhost:5000/api/statistics
- **Login:** http://localhost:5000/login

### الإنتاج:
- **Railway:** https://your-app.railway.app
- **Render:** https://your-app.onrender.com

---

## 📊 APIs متاحة

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/residents` | GET | قائمة السكان |
| `/api/buildings` | GET | قائمة المباني |
| `/api/units` | GET | قائمة الوحدات |
| `/api/stickers` | GET | قائمة الملصقات |
| `/api/parking` | GET | قائمة المواقف |
| `/api/statistics` | GET | إحصائيات عامة |
| `/api/search` | POST | البحث |

---

## 🔐 بيانات الدخول

### Admin:
- **Username:** admin
- **Password:** Admin@2025

---

## 🐛 حل المشاكل السريع

### التطبيق لا يعمل:
```bash
make clean
pip install -r requirements.txt --force-reinstall
make test
```

### الاختبارات تفشل:
```bash
deactivate
rm -rf venv
./setup_dev.sh
```

### قاعدة البيانات مفقودة:
```bash
make db-init
```

---

## 📞 الدعم

- **Email:** housing@imamu.edu.sa
- **GitHub:** https://github.com/Ali5829511/517
- **Issues:** https://github.com/Ali5829511/517/issues

---

## 📚 التوثيق الكامل

- `DEVELOPMENT.md` - دليل التطوير الكامل
- `WORKFLOW.md` - سير العمل التفصيلي
- `DEPLOYMENT_GUIDE.md` - دليل النشر
- `README.md` - نظرة عامة على المشروع

---

**جامعة الإمام محمد بن سعود الإسلامية**  
**نظام إدارة الإسكان الجامعي**
