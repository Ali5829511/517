# test_plate_system.py - اختبارات نظام التعرف على اللوحات
# Plate Recognition System Tests

import sys
import os

# إضافة المسار للاستيراد
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from plate_recognition.main import app
from plate_recognition.database import SessionLocal, init_db
from plate_recognition.models import Vehicle, Camera, Event, Violation

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """إعداد قاعدة البيانات للاختبار"""
    init_db()
    yield


def test_health_check():
    """اختبار فحص صحة التطبيق"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "نظام تحليل اللوحات" in data["service"]


def test_home_page():
    """اختبار الصفحة الرئيسية"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_webhook_plate_valid():
    """اختبار استقبال حدث صحيح"""
    payload = {
        "plate": "ABC1234",
        "timestamp": "2025-01-18T10:30:00",
        "camera_id": "CAM-001",
        "confidence": 95.5,
        "image_url": "https://example.com/test.jpg",
        "vehicle": {"make": "Toyota", "color": "أبيض", "type": "سيدان"},
    }
    response = client.post("/api/webhook/plate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["plate"] == "ABC1234"
    assert data["confidence"] == 95.5


def test_webhook_plate_low_confidence():
    """اختبار رفض حدث بثقة منخفضة"""
    payload = {
        "plate": "XYZ5678",
        "timestamp": "2025-01-18T10:30:00",
        "camera_id": "CAM-002",
        "confidence": 50.0,  # أقل من الحد الأدنى (80)
    }
    response = client.post("/api/webhook/plate", json=payload)
    assert response.status_code == 202


def test_list_events():
    """اختبار استعلام الأحداث"""
    response = client.get("/api/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_violations():
    """اختبار استعلام المخالفات"""
    response = client.get("/api/violations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_export_html():
    """اختبار تصدير HTML"""
    payload = {"format": "html", "filter": {}}
    response = client.post("/api/export", json=payload)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_export_excel():
    """اختبار تصدير Excel"""
    payload = {"format": "excel", "filter": {}}
    response = client.post("/api/export", json=payload)
    assert response.status_code == 200
    assert "spreadsheetml" in response.headers["content-type"]


def test_export_pdf():
    """اختبار تصدير PDF"""
    payload = {"format": "pdf", "filter": {}}
    response = client.post("/api/export", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_export_invalid_format():
    """اختبار تصدير بصيغة غير صحيحة"""
    payload = {"format": "invalid", "filter": {}}
    response = client.post("/api/export", json=payload)
    assert response.status_code == 422  # Validation error


def test_events_with_filters():
    """اختبار استعلام الأحداث مع فلاتر"""
    response = client.get("/api/events?min_confidence=90&plate=ABC1234")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # التحقق من أن جميع النتائج تطابق الفلتر
    for event in data:
        if "confidence" in event:
            assert event["confidence"] >= 90


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
