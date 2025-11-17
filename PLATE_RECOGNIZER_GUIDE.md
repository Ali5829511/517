# دليل نظام تحليل الصور والمخالفات المرورية
# Plate Recognition and Traffic Violations System Guide

## نظرة عامة | Overview

تم تطوير نظام متكامل لتحليل صور السيارات والكشف عن المخالفات المرورية مع التكامل مع أنظمة خارجية.

This system integrates with Plate Recognizer API and Takamul system for comprehensive vehicle management and traffic violation tracking.

## الميزات الجديدة | New Features

### 1. قاعدة بيانات السيارات (Vehicles Database)

جدول شامل لتسجيل جميع السيارات المرتبطة بالسكان:

```sql
- معلومات السيارة الكاملة (Make, Model, Year, Type, Color)
- رقم اللوحة بالعربي والإنجليزي
- ربط مع الساكن المالك
- تاريخ التسجيل وآخر مشاهدة
- حالة السيارة (نشط/متوقف)
```

**API Endpoints:**
- `GET /api/vehicles` - جلب جميع السيارات
- `POST /api/vehicles` - إضافة سيارة جديدة
- `PUT /api/vehicles/<id>` - تحديث معلومات سيارة
- `POST /api/vehicles/search` - البحث برقم اللوحة
- `GET /api/vehicles/statistics` - إحصائيات السيارات

### 2. قاعدة بيانات المخالفات المرورية (Traffic Violations Database)

نظام متكامل لتسجيل ومتابعة المخالفات:

```sql
- نوع المخالفة والوصف
- تاريخ ومكان المخالفة
- قيمة الغرامة
- حالة المخالفة (مفتوح/مدفوع)
- ربط بالسيارة والصورة
- درجة الثقة من التحليل
```

**API Endpoints:**
- `GET /api/violations` - جلب جميع المخالفات
- `POST /api/violations` - إضافة مخالفة جديدة
- `PUT /api/violations/<id>` - تحديث حالة المخالفة
- `POST /api/violations/by-plate` - مخالفات سيارة معينة
- `GET /api/violations/statistics` - إحصائيات المخالفات

### 3. التكامل مع Plate Recognizer API

نظام متقدم للتعرف على لوحات السيارات:

**الميزات:**
- تحليل تلقائي للصور
- استخراج رقم اللوحة بدقة عالية
- التعرف على نوع ولون السيارة
- دعم اللوحات السعودية
- Webhook لاستقبال النتائج تلقائياً

**API Endpoints:**
- `POST /api/plate-recognizer/analyze` - تحليل صورة
- `POST /api/webhooks/plate-recognizer` - webhook endpoint
- `GET /api/plate-recognizer/logs` - سجل التحليلات

**إعداد Webhook في Plate Recognizer:**
1. سجل دخول على https://app.platerecognizer.com
2. انتقل إلى Settings → Webhooks
3. أضف Webhook URL: `https://your-domain.com/api/webhooks/plate-recognizer`
4. اختر الأحداث: "Snapshot Cloud"
5. احفظ الإعدادات

### 4. التكامل مع نظام تكامل (Takamul Integration)

مزامنة تلقائية للبيانات:

**الميزات:**
- جلب بيانات السيارات من تكامل
- جلب بيانات السكان
- إرسال المخالفات إلى تكامل
- سجل كامل للمزامنة

**API Endpoints:**
- `POST /api/takamul/sync` - مزامنة البيانات
- `GET /api/takamul/sync-history` - سجل المزامنة
- `POST /api/takamul/send-violation` - إرسال مخالفة

## التثبيت والإعداد | Installation & Setup

### 1. تطبيق التغييرات على قاعدة البيانات

```bash
# تطبيق الجداول الجديدة
python apply_migrations.py
```

### 2. إعداد متغيرات البيئة

انسخ `.env.example` إلى `.env` وقم بتعبئة القيم:

```bash
cp .env.example .env
```

قم بتحديث الملف:

```env
# Plate Recognizer API
PLATE_RECOGNIZER_TOKEN=your-token-here

# Takamul Integration
TAKAMUL_API_URL=https://takamul-api-url.com
TAKAMUL_API_KEY=your-api-key-here
```

### 3. تثبيت المكتبات المطلوبة

```bash
pip install -r requirements.txt
```

## أمثلة الاستخدام | Usage Examples

### مثال 1: إضافة سيارة جديدة

```python
import requests

url = "http://localhost:5000/api/vehicles"
headers = {"Content-Type": "application/json"}
data = {
    "resident_id": 1,
    "plate_number": "ABC 1234",
    "plate_arabic": "أ ب ج 1234",
    "plate_english": "ABC 1234",
    "vehicle_make": "Toyota",
    "vehicle_model": "Camry",
    "vehicle_year": 2023,
    "vehicle_type": "سيدان",
    "vehicle_color": "أبيض"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### مثال 2: تحليل صورة سيارة

```python
import requests

url = "http://localhost:5000/api/plate-recognizer/analyze"
files = {"image": open("car_image.jpg", "rb")}

response = requests.post(url, files=files)
result = response.json()

print(f"رقم اللوحة: {result['plate_number']}")
print(f"درجة الثقة: {result['confidence']}%")
```

### مثال 3: إضافة مخالفة

```python
import requests

url = "http://localhost:5000/api/violations"
data = {
    "vehicle_id": 1,
    "plate_number": "ABC 1234",
    "violation_type": "تجاوز السرعة",
    "violation_description": "تجاوز السرعة المحددة بـ 20 كم/س",
    "violation_location": "شارع الملك فهد",
    "fine_amount": 500.00,
    "confidence_score": 95
}

response = requests.post(url, json=data)
print(response.json())
```

### مثال 4: مزامنة مع تكامل

```python
import requests

url = "http://localhost:5000/api/takamul/sync"
data = {"sync_type": "vehicles"}

response = requests.post(url, json=data)
result = response.json()

print(f"تم مزامنة {result['synced']} سيارة من أصل {result['total']}")
```

## هيكل قاعدة البيانات | Database Schema

### جدول vehicles

| العمود | النوع | الوصف |
|--------|------|-------|
| id | INTEGER | المعرف الفريد |
| resident_id | INTEGER | معرف الساكن المالك |
| plate_number | TEXT | رقم اللوحة |
| plate_arabic | TEXT | اللوحة بالعربي |
| plate_english | TEXT | اللوحة بالإنجليزي |
| vehicle_make | TEXT | الماركة |
| vehicle_model | TEXT | الموديل |
| vehicle_year | INTEGER | سنة الصنع |
| vehicle_type | TEXT | نوع السيارة |
| vehicle_color | TEXT | اللون |
| registration_date | TEXT | تاريخ التسجيل |
| last_seen | TEXT | آخر مشاهدة |
| status | TEXT | الحالة |
| notes | TEXT | ملاحظات |

### جدول traffic_violations

| العمود | النوع | الوصف |
|--------|------|-------|
| id | INTEGER | المعرف الفريد |
| vehicle_id | INTEGER | معرف السيارة |
| plate_number | TEXT | رقم اللوحة |
| violation_type | TEXT | نوع المخالفة |
| violation_date | TEXT | تاريخ المخالفة |
| violation_location | TEXT | مكان المخالفة |
| violation_description | TEXT | وصف المخالفة |
| fine_amount | REAL | قيمة الغرامة |
| status | TEXT | الحالة |
| payment_date | TEXT | تاريخ الدفع |
| image_path | TEXT | مسار الصورة |
| confidence_score | INTEGER | درجة الثقة |
| notes | TEXT | ملاحظات |

## الأمان | Security

### حماية API Endpoints

جميع endpoints محمية بـ `@login_required` ما عدا webhook endpoint:

```python
@app.route("/api/vehicles")
@login_required  # يتطلب تسجيل دخول
def api_get_vehicles():
    # ...
```

### حماية Webhook

يُنصح بإضافة توثيق للـ webhook:

```python
# يمكن إضافة secret token للتحقق
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

@app.route("/api/webhooks/plate-recognizer", methods=["POST"])
def webhook_plate_recognizer():
    # التحقق من التوثيق
    token = request.headers.get("X-Webhook-Token")
    if token != WEBHOOK_SECRET:
        return jsonify({"error": "Unauthorized"}), 401
    # ...
```

## الصيانة | Maintenance

### عرض الإحصائيات

```bash
# الحصول على إحصائيات السيارات
curl http://localhost:5000/api/vehicles/statistics

# الحصول على إحصائيات المخالفات
curl http://localhost:5000/api/violations/statistics
```

### نسخ احتياطي للبيانات

```bash
# نسخ قاعدة البيانات
cp housing_database.db housing_database_backup_$(date +%Y%m%d).db
```

### تنظيف السجلات القديمة

```sql
-- حذف سجلات أقدم من 6 أشهر
DELETE FROM plate_recognizer_log 
WHERE processing_date < datetime('now', '-6 months');

DELETE FROM takamul_integration 
WHERE sync_date < datetime('now', '-6 months');
```

## الاختبار | Testing

### اختبار التكامل مع Plate Recognizer

```bash
# اختبار تحليل صورة
curl -X POST http://localhost:5000/api/plate-recognizer/analyze \
  -F "image=@test_car.jpg"
```

### اختبار Webhook

```bash
# محاكاة webhook من Plate Recognizer
curl -X POST http://localhost:5000/api/webhooks/plate-recognizer \
  -H "Content-Type: application/json" \
  -d '{
    "results": [{
      "plate": "ABC1234",
      "score": 0.95,
      "vehicle": {
        "type": "Sedan",
        "color": [{"color": "white"}]
      }
    }]
  }'
```

## استكشاف الأخطاء | Troubleshooting

### مشكلة: Plate Recognizer لا يعمل

**الحل:**
1. تحقق من صحة `PLATE_RECOGNIZER_TOKEN`
2. تأكد من وجود رصيد كافٍ في الحساب
3. راجع السجلات: `tail -f logs/app.log`

### مشكلة: فشل المزامنة مع تكامل

**الحل:**
1. تحقق من `TAKAMUL_API_URL` و `TAKAMUL_API_KEY`
2. تأكد من إمكانية الوصول إلى API
3. راجع سجل المزامنة: `GET /api/takamul/sync-history`

### مشكلة: الجداول الجديدة غير موجودة

**الحل:**
```bash
# إعادة تطبيق التغييرات
python apply_migrations.py
```

## الدعم | Support

للحصول على الدعم:
- راجع الوثائق: `README.md`
- راجع سجل التغييرات: `git log`
- تحقق من السجلات: `logs/app.log`

## التطوير المستقبلي | Future Development

### ميزات مقترحة:
- [ ] تنبيهات تلقائية للمخالفات
- [ ] تقارير شهرية للمخالفات
- [ ] لوحة تحكم تفاعلية للمخالفات
- [ ] تكامل مع نظام الدفع الإلكتروني
- [ ] تطبيق موبايل للسكان
- [ ] كاميرات مراقبة مباشرة
- [ ] تحليل الفيديو بالوقت الفعلي

---

**تم التطوير بواسطة:** Manus AI  
**التاريخ:** نوفمبر 2025  
**الإصدار:** 1.0.0
