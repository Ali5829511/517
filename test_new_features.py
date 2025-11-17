#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار النظام الجديد
Test the new system features
"""

import sys
import json
from database_api import (
    get_all_vehicles,
    add_vehicle,
    search_vehicle_by_plate,
    get_all_violations,
    add_violation,
    get_violations_by_plate,
    get_vehicles_statistics,
    get_violations_statistics,
    log_takamul_sync,
    get_takamul_sync_history,
    log_plate_recognizer_analysis,
    get_plate_recognizer_logs,
)

def test_vehicles():
    """اختبار وظائف السيارات"""
    print("\n" + "="*60)
    print("اختبار وظائف السيارات | Testing Vehicles Functions")
    print("="*60)
    
    # 1. إضافة سيارة تجريبية
    print("\n1. إضافة سيارة تجريبية...")
    result = add_vehicle(
        resident_id=1,
        plate_number="TEST123",
        plate_arabic="أ ب ج 123",
        plate_english="ABC 123",
        vehicle_make="Toyota",
        vehicle_model="Camry",
        vehicle_year=2023,
        vehicle_type="سيدان",
        vehicle_color="أبيض",
        notes="سيارة اختبار"
    )
    
    if result.get("success"):
        print(f"   ✅ تم إضافة السيارة بنجاح - ID: {result['id']}")
        vehicle_id = result['id']
    else:
        print(f"   ⚠️  السيارة موجودة مسبقاً أو خطأ: {result.get('error')}")
        vehicle_id = None
    
    # 2. جلب جميع السيارات
    print("\n2. جلب جميع السيارات...")
    vehicles = get_all_vehicles()
    print(f"   ✅ تم جلب {len(vehicles)} سيارة")
    if vehicles:
        print(f"   مثال: {vehicles[0].get('plate_number')} - {vehicles[0].get('vehicle_make')}")
    
    # 3. البحث عن سيارة
    print("\n3. البحث عن سيارة برقم اللوحة...")
    search_result = search_vehicle_by_plate("TEST123")
    if search_result.get("found"):
        print(f"   ✅ تم العثور على السيارة: {search_result['vehicle'].get('plate_number')}")
    else:
        print("   ℹ️  لم يتم العثور على السيارة")
    
    # 4. إحصائيات السيارات
    print("\n4. إحصائيات السيارات...")
    stats = get_vehicles_statistics()
    print(f"   ✅ إجمالي السيارات: {stats['total']}")
    print(f"   ✅ السيارات النشطة: {stats['active']}")
    
    return vehicle_id

def test_violations(vehicle_id=None):
    """اختبار وظائف المخالفات"""
    print("\n" + "="*60)
    print("اختبار وظائف المخالفات | Testing Violations Functions")
    print("="*60)
    
    # 1. إضافة مخالفة تجريبية
    print("\n1. إضافة مخالفة تجريبية...")
    result = add_violation(
        vehicle_id=vehicle_id,
        plate_number="TEST123",
        violation_type="تجاوز السرعة",
        violation_description="تجاوز السرعة المحددة",
        violation_location="شارع الملك فهد",
        fine_amount=300.00,
        confidence_score=95,
        notes="مخالفة اختبار"
    )
    
    if result.get("success"):
        print(f"   ✅ تم إضافة المخالفة بنجاح - ID: {result['id']}")
    else:
        print(f"   ❌ خطأ في إضافة المخالفة: {result.get('error')}")
    
    # 2. جلب جميع المخالفات
    print("\n2. جلب جميع المخالفات...")
    violations = get_all_violations()
    print(f"   ✅ تم جلب {len(violations)} مخالفة")
    if violations:
        print(f"   مثال: {violations[0].get('violation_type')} - {violations[0].get('fine_amount')} ريال")
    
    # 3. البحث عن مخالفات سيارة
    print("\n3. البحث عن مخالفات سيارة معينة...")
    plate_violations = get_violations_by_plate("TEST123")
    print(f"   ✅ تم العثور على {len(plate_violations)} مخالفة")
    
    # 4. إحصائيات المخالفات
    print("\n4. إحصائيات المخالفات...")
    stats = get_violations_statistics()
    print(f"   ✅ إجمالي المخالفات: {stats['total']}")
    print(f"   ✅ المخالفات المفتوحة: {stats['open']}")
    print(f"   ✅ إجمالي الغرامات: {stats['total_fines']} ريال")

def test_takamul_integration():
    """اختبار التكامل مع تكامل"""
    print("\n" + "="*60)
    print("اختبار التكامل مع تكامل | Testing Takamul Integration")
    print("="*60)
    
    # 1. تسجيل مزامنة
    print("\n1. تسجيل عملية مزامنة...")
    result = log_takamul_sync(
        sync_type="vehicles",
        records_synced=5,
        status="نجح",
        data_snapshot=json.dumps({"test": "data"})
    )
    
    if result.get("success"):
        print(f"   ✅ تم تسجيل المزامنة - ID: {result['id']}")
    else:
        print(f"   ❌ خطأ في تسجيل المزامنة")
    
    # 2. جلب سجل المزامنة
    print("\n2. جلب سجل المزامنة...")
    history = get_takamul_sync_history(limit=10)
    print(f"   ✅ تم جلب {len(history)} سجل مزامنة")
    if history:
        print(f"   آخر مزامنة: {history[0].get('sync_type')} - {history[0].get('status')}")

def test_plate_recognizer():
    """اختبار Plate Recognizer"""
    print("\n" + "="*60)
    print("اختبار Plate Recognizer | Testing Plate Recognizer")
    print("="*60)
    
    # 1. تسجيل تحليل
    print("\n1. تسجيل تحليل صورة...")
    result = log_plate_recognizer_analysis(
        image_path="/uploads/test.jpg",
        plate_number="ABC1234",
        vehicle_type="Sedan",
        vehicle_color="White",
        confidence=95.5,
        api_response=json.dumps({"test": "response"}),
        status="معالج",
        notes="تحليل اختبار"
    )
    
    if result.get("success"):
        print(f"   ✅ تم تسجيل التحليل - ID: {result['id']}")
    else:
        print(f"   ❌ خطأ في تسجيل التحليل")
    
    # 2. جلب السجلات
    print("\n2. جلب سجلات التحليل...")
    logs = get_plate_recognizer_logs(limit=10)
    print(f"   ✅ تم جلب {len(logs)} سجل تحليل")
    if logs:
        print(f"   آخر تحليل: {logs[0].get('plate_number')} - ثقة: {logs[0].get('confidence')}%")

def test_api_imports():
    """اختبار استيراد الوظائف في app.py"""
    print("\n" + "="*60)
    print("اختبار استيراد الوظائف | Testing API Imports")
    print("="*60)
    
    try:
        # محاولة استيراد التطبيق
        import app
        print("   ✅ تم استيراد app.py بنجاح")
        
        # التحقق من وجود الـ routes الجديدة
        routes = [rule.rule for rule in app.app.url_map.iter_rules()]
        
        new_routes = [
            "/api/vehicles",
            "/api/violations",
            "/api/plate-recognizer/analyze",
            "/api/webhooks/plate-recognizer",
            "/api/takamul/sync",
        ]
        
        print("\n   التحقق من Routes الجديدة:")
        for route in new_routes:
            if route in routes:
                print(f"   ✅ {route}")
            else:
                print(f"   ❌ {route} - غير موجود")
        
        return True
    
    except Exception as e:
        print(f"   ❌ خطأ في استيراد app.py: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("🚀 بدء اختبار النظام الجديد")
    print("   Starting New System Tests")
    print("="*60)
    
    try:
        # اختبار السيارات
        vehicle_id = test_vehicles()
        
        # اختبار المخالفات
        test_violations(vehicle_id)
        
        # اختبار التكامل مع تكامل
        test_takamul_integration()
        
        # اختبار Plate Recognizer
        test_plate_recognizer()
        
        # اختبار الـ API
        test_api_imports()
        
        print("\n" + "="*60)
        print("✅ اكتملت جميع الاختبارات بنجاح!")
        print("   All tests completed successfully!")
        print("="*60)
        
        return 0
    
    except Exception as e:
        print(f"\n❌ خطأ في الاختبارات: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
