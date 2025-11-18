# أمثلة استخدام نظام التعرف على اللوحات
# Plate Recognition System Usage Examples

## 📌 نظرة عامة

هذا الملف يحتوي على أمثلة عملية لاستخدام نظام التعرف على اللوحات.

---

## 🚀 البدء السريع

### 1. تشغيل النظام

```bash
# من المجلد الرئيسي
./run_plate_system.sh

# أو من داخل مجلد plate_recognition
cd plate_recognition
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. فتح الواجهة

افتح المتصفح على: http://localhost:8000

---

## 📡 أمثلة API

### مثال 1: إرسال حدث تعرف بسيط

```bash
curl -X POST "http://localhost:8000/api/webhook/plate" \
  -H "Content-Type: application/json" \
  -d '{
    "plate": "ABC1234",
    "timestamp": "2025-01-18T10:30:00",
    "camera_id": "CAM-001",
    "confidence": 95.5
  }'
```

### مثال 2: إرسال حدث مع بيانات المركبة

```bash
curl -X POST "http://localhost:8000/api/webhook/plate" \
  -H "Content-Type: application/json" \
  -d '{
    "plate": "XYZ5678",
    "timestamp": "2025-01-18T11:00:00",
    "camera_id": "CAM-002",
    "confidence": 92.3,
    "image_url": "https://example.com/images/xyz5678.jpg",
    "vehicle": {
      "make": "Toyota",
      "color": "أبيض",
      "type": "سيدان"
    }
  }'
```

### مثال 3: استعلام الأحداث - جميع الأحداث

```bash
curl "http://localhost:8000/api/events"
```

### مثال 4: استعلام الأحداث - مع فلاتر

```bash
# فلترة حسب الثقة
curl "http://localhost:8000/api/events?min_confidence=90"

# فلترة حسب اللوحة
curl "http://localhost:8000/api/events?plate=ABC1234"

# فلترة حسب الكاميرا
curl "http://localhost:8000/api/events?camera_id=CAM-001"

# فلاتر متعددة
curl "http://localhost:8000/api/events?min_confidence=85&camera_id=CAM-002&plate=XYZ"
```

### مثال 5: استعلام المخالفات

```bash
curl "http://localhost:8000/api/violations"
```

### مثال 6: تصدير إلى HTML

```bash
curl -X POST "http://localhost:8000/api/export" \
  -H "Content-Type: application/json" \
  -d '{"format": "html"}' \
  > report.html
```

### مثال 7: تصدير إلى Excel مع فلتر

```bash
curl -X POST "http://localhost:8000/api/export" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "excel",
    "filter": {
      "min_confidence": 85,
      "start": "2025-01-01T00:00:00",
      "end": "2025-01-31T23:59:59"
    }
  }' \
  --output events.xlsx
```

### مثال 8: تصدير إلى PDF

```bash
curl -X POST "http://localhost:8000/api/export" \
  -H "Content-Type: application/json" \
  -d '{"format": "pdf"}' \
  --output report.pdf
```

### مثال 9: فحص صحة النظام

```bash
curl "http://localhost:8000/health"
```

---

## 🐍 أمثلة Python

### مثال 1: إرسال حدث باستخدام requests

```python
import requests
from datetime import datetime

url = "http://localhost:8000/api/webhook/plate"
data = {
    "plate": "ABC1234",
    "timestamp": datetime.now().isoformat(),
    "camera_id": "CAM-001",
    "confidence": 95.5,
    "vehicle": {
        "make": "Toyota",
        "color": "أبيض",
        "type": "سيدان"
    }
}

response = requests.post(url, json=data)
print(response.json())
```

### مثال 2: استعلام الأحداث

```python
import requests

url = "http://localhost:8000/api/events"
params = {
    "min_confidence": 85,
    "plate": "ABC"
}

response = requests.get(url, params=params)
events = response.json()

for event in events:
    print(f"اللوحة: {event['plate']}, الثقة: {event['confidence']}%")
```

### مثال 3: تصدير وحفظ Excel

```python
import requests

url = "http://localhost:8000/api/export"
data = {
    "format": "excel",
    "filter": {
        "min_confidence": 80
    }
}

response = requests.post(url, json=data)

with open("events.xlsx", "wb") as f:
    f.write(response.content)
    
print("✅ تم حفظ الملف")
```

### مثال 4: استيراد من Excel

```python
import requests

url = "http://localhost:8000/api/import/excel"
files = {"file": open("events.xlsx", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### مثال 5: محاكاة كاميرا تعرف

```python
import requests
import time
from datetime import datetime
import random

def simulate_camera(camera_id, plates):
    """محاكاة كاميرا ترسل أحداث تعرف"""
    url = "http://localhost:8000/api/webhook/plate"
    
    while True:
        plate = random.choice(plates)
        confidence = random.uniform(80, 99)
        
        data = {
            "plate": plate,
            "timestamp": datetime.now().isoformat(),
            "camera_id": camera_id,
            "confidence": round(confidence, 1)
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(f"✅ {camera_id}: {plate} ({confidence:.1f}%)")
            else:
                print(f"❌ {camera_id}: خطأ {response.status_code}")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        
        time.sleep(5)  # انتظر 5 ثواني

# استخدام
plates = ["ABC1234", "XYZ5678", "DEF9012", "GHI3456"]
simulate_camera("CAM-001", plates)
```

---

## 🧪 أمثلة الاختبار

### اختبار كامل للنظام

```python
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_full_workflow():
    """اختبار كامل للنظام"""
    
    # 1. فحص الصحة
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✅ فحص الصحة ناجح")
    
    # 2. إرسال حدث
    data = {
        "plate": "TEST123",
        "timestamp": datetime.now().isoformat(),
        "camera_id": "CAM-TEST",
        "confidence": 95.0
    }
    response = requests.post(f"{BASE_URL}/api/webhook/plate", json=data)
    assert response.status_code == 200
    print("✅ إرسال حدث ناجح")
    
    # 3. استعلام الأحداث
    response = requests.get(f"{BASE_URL}/api/events?plate=TEST123")
    events = response.json()
    assert len(events) > 0
    print(f"✅ استعلام الأحداث ناجح ({len(events)} حدث)")
    
    # 4. تصدير HTML
    response = requests.post(f"{BASE_URL}/api/export", json={"format": "html"})
    assert response.status_code == 200
    print("✅ تصدير HTML ناجح")
    
    print("\n🎉 جميع الاختبارات نجحت!")

if __name__ == "__main__":
    test_full_workflow()
```

---

## 📊 إنشاء تقارير مخصصة

### مثال: تقرير يومي

```python
import requests
from datetime import datetime, timedelta
import pandas as pd

def daily_report():
    """إنشاء تقرير يومي"""
    
    # تحديد الفترة (اليوم)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    # استعلام الأحداث
    url = "http://localhost:8000/api/events"
    params = {
        "start": today.isoformat(),
        "end": tomorrow.isoformat()
    }
    
    response = requests.get(url, params=params)
    events = response.json()
    
    # تحليل البيانات
    df = pd.DataFrame(events)
    
    print(f"📊 تقرير يوم {today.date()}")
    print("=" * 50)
    print(f"إجمالي الأحداث: {len(df)}")
    print(f"متوسط الثقة: {df['confidence'].mean():.1f}%")
    print(f"عدد اللوحات الفريدة: {df['plate'].nunique()}")
    print(f"أكثر لوحة تكراراً: {df['plate'].mode()[0] if len(df) > 0 else 'N/A'}")
    
    # استعلام المخالفات
    response = requests.get("http://localhost:8000/api/violations")
    violations = response.json()
    print(f"المخالفات المفتوحة: {len([v for v in violations if v['status'] == 'open'])}")

daily_report()
```

---

## 🔧 التكامل مع Plate Recognizer

### مثال: استقبال من Plate Recognizer Webhook

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/plate-recognizer-webhook")
async def handle_plate_recognizer(request: Request):
    """استقبال webhook من Plate Recognizer وإعادة إرساله لنظامنا"""
    
    data = await request.json()
    
    # تحويل البيانات لصيغتنا
    our_data = {
        "plate": data['results'][0]['plate'],
        "timestamp": data['timestamp'],
        "camera_id": data.get('camera_id', 'UNKNOWN'),
        "confidence": data['results'][0]['score'] * 100,
        "image_url": data.get('image_url'),
        "vehicle": {
            "make": data['results'][0].get('vehicle', {}).get('make'),
            "color": data['results'][0].get('vehicle', {}).get('color'),
            "type": data['results'][0].get('vehicle', {}).get('type')
        }
    }
    
    # إرسال لنظامنا
    import requests
    response = requests.post(
        "http://localhost:8000/api/webhook/plate",
        json=our_data
    )
    
    return {"status": "ok", "forwarded": True}
```

---

## 🎯 سيناريوهات الاستخدام

### سيناريو 1: مراقبة موقف سيارات

```python
import requests
from datetime import datetime, timedelta

def check_parking_violations():
    """فحص مخالفات الموقف"""
    
    # الحصول على أحداث آخر 24 ساعة
    url = "http://localhost:8000/api/events"
    yesterday = datetime.now() - timedelta(days=1)
    
    params = {"start": yesterday.isoformat()}
    response = requests.get(url, params=params)
    events = response.json()
    
    # تحليل التكرار
    from collections import Counter
    plates = [e['plate'] for e in events]
    plate_counts = Counter(plates)
    
    # تحديد المخالفين
    violators = {p: c for p, c in plate_counts.items() if c >= 3}
    
    print(f"🚗 إجمالي السيارات: {len(plate_counts)}")
    print(f"⚠️  مخالفات التكرار: {len(violators)}")
    
    for plate, count in violators.items():
        print(f"  - {plate}: {count} مرات")

check_parking_violations()
```

### سيناريو 2: تنبيه فوري للمخالفات

```python
import requests
import time

def alert_monitor():
    """مراقبة المخالفات والتنبيه"""
    
    last_check = None
    
    while True:
        response = requests.get("http://localhost:8000/api/violations")
        violations = response.json()
        
        # فلترة المخالفات الجديدة المفتوحة
        new_violations = [
            v for v in violations 
            if v['status'] == 'open'
        ]
        
        if new_violations:
            print(f"🚨 تنبيه: {len(new_violations)} مخالفة مفتوحة!")
            for v in new_violations:
                print(f"  ⚠️  {v['plate']}: {v['violation_type']}")
        
        time.sleep(30)  # فحص كل 30 ثانية

# استخدام
# alert_monitor()
```

---

## 📝 ملاحظات مهمة

### الحد الأدنى للثقة
- افتراضياً: 80%
- يمكن تعديله في `.env`: `CONFIDENCE_MIN=85`

### حدود API
- لا توجد حدود افتراضياً
- يُنصح بإضافة rate limiting في الإنتاج

### أفضل الممارسات
1. استخدم HTTPS في الإنتاج
2. أضف مصادقة API
3. راقب السجلات بانتظام
4. احتفظ بنسخة احتياطية من قاعدة البيانات

---

**جاهز للاستخدام! 🚀**

للمزيد من المعلومات، راجع:
- [PLATE_RECOGNITION_GUIDE.md](PLATE_RECOGNITION_GUIDE.md)
- [plate_recognition/README.md](plate_recognition/README.md)
- [plate_recognition/QUICKSTART.md](plate_recognition/QUICKSTART.md)
