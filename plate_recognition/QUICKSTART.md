# دليل التشغيل السريع - نظام التعرف على اللوحات
# Quick Start Guide - Plate Recognition System

## 🚀 التشغيل في خطوة واحدة

### على Linux/Mac:
```bash
./run_plate_system.sh
```

### على Windows:
```bash
cd plate_recognition
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📍 الوصول للنظام

بعد التشغيل، افتح المتصفح على:

- **الصفحة الرئيسية:** http://localhost:8000
- **التوثيق التفاعلي (Swagger):** http://localhost:8000/docs
- **التوثيق البديل (ReDoc):** http://localhost:8000/redoc

## 🧪 اختبار النظام

```bash
# تشغيل جميع الاختبارات
python -m pytest test_plate_system.py -v

# اختبار واحد محدد
python -m pytest test_plate_system.py::test_health_check -v
```

## 📤 أمثلة الاستخدام

### 1. إرسال حدث تعرف جديد (Webhook)

```bash
curl -X POST "http://localhost:8000/api/webhook/plate" \
  -H "Content-Type: application/json" \
  -d '{
    "plate": "ABC1234",
    "timestamp": "2025-01-18T10:30:00",
    "camera_id": "CAM-001",
    "confidence": 95.5,
    "vehicle": {
      "make": "Toyota",
      "color": "أبيض",
      "type": "سيدان"
    }
  }'
```

### 2. استعلام الأحداث

```bash
curl "http://localhost:8000/api/events?min_confidence=85&plate=ABC1234"
```

### 3. استعلام المخالفات

```bash
curl "http://localhost:8000/api/violations"
```

### 4. تصدير إلى Excel

```bash
curl -X POST "http://localhost:8000/api/export" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "excel",
    "filter": {
      "min_confidence": 80
    }
  }' --output events.xlsx
```

## ⚙️ التخصيص

عدّل ملف `.env` لتخصيص الإعدادات:

```ini
CONFIDENCE_MIN=80              # الحد الأدنى للثقة
REPEAT_THRESHOLD_COUNT=3       # عدد التكرار للمخالفة
REPEAT_WINDOW_HOURS=24         # فترة التكرار بالساعات
ALLOWED_START=06:00            # وقت البدء المسموح
ALLOWED_END=22:00              # وقت الانتهاء المسموح
```

## 🗄️ قاعدة البيانات

يستخدم النظام SQLite افتراضياً (ملف `plates.db`).

### التحويل إلى PostgreSQL:

1. ثبّت psycopg2:
```bash
pip install psycopg2-binary
```

2. عدّل DATABASE_URL في `.env`:
```ini
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/plates_db
```

## 📊 الواجهة العربية

الواجهة مصممة بالكامل بالعربية وتشمل:
- عرض الأحداث في جدول تفاعلي
- قائمة المخالفات مع الحالة
- أدوات التصدير (Excel, PDF, HTML)
- نموذج استيراد من Excel
- إحصائيات سريعة

## 🐛 استكشاف الأخطاء

### المشكلة: الخادم لا يبدأ
```bash
# تأكد من تثبيت المكتبات
pip install -r ../requirements.txt
```

### المشكلة: خطأ في قاعدة البيانات
```bash
# احذف قاعدة البيانات وأعد إنشائها
cd plate_recognition
rm plates.db
python -c "from database import init_db; init_db()"
```

### المشكلة: القوالب غير موجودة
```bash
# تأكد من وجود المجلد
ls plate_recognition/templates/index.html
```

## 📚 المزيد من المعلومات

راجع ملف [README.md](README.md) للحصول على التوثيق الكامل.

---

**جاهز للاستخدام! 🎉**
