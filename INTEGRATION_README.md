# نظام التكامل مع Plate Recognizer و تكامل
# Plate Recognizer and Takamul Integration System

## ملخص التغييرات | Changes Summary

تم إضافة نظام متكامل لإدارة السيارات والمخالفات المرورية مع التكامل مع أنظمة خارجية.

### الميزات الجديدة | New Features

#### 1. قاعدة بيانات السيارات (vehicles)
- جدول كامل لتسجيل جميع السيارات
- ربط مع السكان
- معلومات تفصيلية (Make, Model, Year, Type, Color)
- رقم اللوحة بالعربي والإنجليزي

#### 2. قاعدة بيانات المخالفات المرورية (traffic_violations)
- تسجيل المخالفات المرورية
- ربط بالسيارات والسكان
- حالة المخالفة والغرامات
- صور المخالفات

#### 3. التكامل مع Plate Recognizer API
- تحليل تلقائي لصور السيارات
- استخراج رقم اللوحة
- التعرف على نوع ولون السيارة
- Webhook endpoint لاستقبال النتائج

#### 4. التكامل مع نظام تكامل (Takamul)
- مزامنة بيانات السيارات
- جلب بيانات السكان
- إرسال المخالفات
- سجل كامل للمزامنة

## الملفات الجديدة | New Files

```
├── migrations/
│   └── 001_add_vehicles_and_violations.sql  # تعريف الجداول الجديدة
├── apply_migrations.py                       # تطبيق التغييرات على قاعدة البيانات
├── plate_recognizer_client.py               # عميل Plate Recognizer API
├── takamul_client.py                        # عميل نظام تكامل
├── test_new_features.py                     # اختبارات النظام الجديد
├── PLATE_RECOGNIZER_GUIDE.md                # دليل شامل للنظام
└── INTEGRATION_README.md                    # هذا الملف
```

## التثبيت السريع | Quick Installation

### 1. تطبيق تغييرات قاعدة البيانات

```bash
python apply_migrations.py
```

### 2. تحديث متغيرات البيئة

أضف إلى ملف `.env`:

```env
# Plate Recognizer
PLATE_RECOGNIZER_TOKEN=your-token-here

# Takamul Integration
TAKAMUL_API_URL=https://takamul-api-url.com
TAKAMUL_API_KEY=your-api-key-here
```

### 3. تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### 4. تشغيل الاختبارات

```bash
python test_new_features.py
```

## API Endpoints الجديدة | New API Endpoints

### السيارات (Vehicles)

```
GET    /api/vehicles              - جلب جميع السيارات
POST   /api/vehicles              - إضافة سيارة جديدة
PUT    /api/vehicles/<id>         - تحديث سيارة
POST   /api/vehicles/search       - البحث برقم اللوحة
GET    /api/vehicles/statistics   - إحصائيات السيارات
```

### المخالفات (Violations)

```
GET    /api/violations            - جلب جميع المخالفات
POST   /api/violations            - إضافة مخالفة
PUT    /api/violations/<id>       - تحديث مخالفة
POST   /api/violations/by-plate   - مخالفات سيارة معينة
GET    /api/violations/statistics - إحصائيات المخالفات
```

### Plate Recognizer

```
POST   /api/plate-recognizer/analyze      - تحليل صورة
POST   /api/webhooks/plate-recognizer     - webhook endpoint
GET    /api/plate-recognizer/logs         - سجل التحليلات
```

### تكامل (Takamul)

```
POST   /api/takamul/sync               - مزامنة البيانات
GET    /api/takamul/sync-history       - سجل المزامنة
POST   /api/takamul/send-violation     - إرسال مخالفة
```

## أمثلة الاستخدام | Usage Examples

### إضافة سيارة

```bash
curl -X POST http://localhost:5000/api/vehicles \
  -H "Content-Type: application/json" \
  -d '{
    "resident_id": 1,
    "plate_number": "ABC1234",
    "vehicle_make": "Toyota",
    "vehicle_model": "Camry",
    "vehicle_year": 2023,
    "vehicle_type": "سيدان",
    "vehicle_color": "أبيض"
  }'
```

### تحليل صورة سيارة

```bash
curl -X POST http://localhost:5000/api/plate-recognizer/analyze \
  -F "image=@car_image.jpg"
```

### إضافة مخالفة

```bash
curl -X POST http://localhost:5000/api/violations \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": 1,
    "plate_number": "ABC1234",
    "violation_type": "تجاوز السرعة",
    "fine_amount": 500.00
  }'
```

## إعداد Webhook في Plate Recognizer

1. سجل دخول على https://app.platerecognizer.com
2. انتقل إلى **Settings** → **Webhooks**
3. أضف URL جديد:
   ```
   https://your-domain.com/api/webhooks/plate-recognizer
   ```
4. اختر الأحداث: **Snapshot Cloud**
5. احفظ الإعدادات

## الأمان | Security

### API Protection
جميع endpoints محمية بـ `@login_required` ما عدا webhook endpoint.

### Webhook Security
يُنصح بإضافة secret token للتحقق من صحة الطلبات:

```env
WEBHOOK_SECRET=your-secret-token
```

## الاختبار | Testing

### اختبار كامل للنظام

```bash
python test_new_features.py
```

### اختبار يدوي

```bash
# تشغيل السيرفر
python app.py

# في نافذة أخرى - اختبار API
curl http://localhost:5000/api/vehicles/statistics
curl http://localhost:5000/api/violations/statistics
```

## المراقبة | Monitoring

### عرض إحصائيات السيارات

```bash
curl http://localhost:5000/api/vehicles/statistics
```

### عرض إحصائيات المخالفات

```bash
curl http://localhost:5000/api/violations/statistics
```

### عرض سجل Plate Recognizer

```bash
curl http://localhost:5000/api/plate-recognizer/logs
```

### عرض سجل تكامل

```bash
curl http://localhost:5000/api/takamul/sync-history
```

## الصيانة | Maintenance

### نسخ احتياطي

```bash
# نسخ قاعدة البيانات
cp housing_database.db housing_database_backup_$(date +%Y%m%d).db

# نسخ الصور
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/
```

### تنظيف السجلات القديمة

```sql
-- حذف سجلات أقدر من 6 أشهر
DELETE FROM plate_recognizer_log 
WHERE processing_date < datetime('now', '-6 months');

DELETE FROM takamul_integration 
WHERE sync_date < datetime('now', '-6 months');
```

## الوثائق | Documentation

للمزيد من التفاصيل، راجع:
- [PLATE_RECOGNIZER_GUIDE.md](PLATE_RECOGNIZER_GUIDE.md) - دليل شامل
- [README.md](README.md) - الوثائق الرئيسية
- [DEVELOPMENT.md](DEVELOPMENT.md) - دليل التطوير

## المساهمة | Contributing

عند إضافة ميزات جديدة:
1. أنشئ branch جديد
2. اختبر التغييرات محلياً
3. شغل الاختبارات: `python test_new_features.py`
4. أنشئ Pull Request

## الدعم | Support

للحصول على الدعم:
- راجع الوثائق
- تحقق من السجلات: `logs/app.log`
- أنشئ Issue على GitHub

---

**تم التطوير:** نوفمبر 2025  
**الإصدار:** 1.0.0  
**المطور:** Manus AI
