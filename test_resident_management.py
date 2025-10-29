#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبارات لوظائف إدارة السكان (CRUD operations)
"""

from database_api import (
    get_available_units, 
    add_resident, 
    update_resident, 
    checkout_resident, 
    delete_resident
)

def test_resident_lifecycle():
    """اختبار دورة حياة الساكن الكاملة"""
    
    # 1. الحصول على الوحدات الشاغرة
    print("1. اختبار الحصول على الوحدات الشاغرة...")
    units = get_available_units()
    assert len(units) > 0, "يجب أن تكون هناك وحدات شاغرة"
    print(f"   ✓ تم العثور على {len(units)} وحدة شاغرة")
    
    # 2. إضافة ساكن جديد
    print("\n2. اختبار إضافة ساكن جديد...")
    test_resident = {
        'name': 'اختبار ساكن جديد',
        'national_id': '1111111111',
        'phone': '0501111111',
        'email': 'test_new@test.com',
        'unit_id': units[0]['id'],
        'move_in_date': '2025-10-29',
        'status': 'نشط'
    }
    result = add_resident(test_resident)
    assert result['success'], f"فشل في إضافة الساكن: {result.get('error')}"
    resident_id = result['id']
    print(f"   ✓ تم إضافة الساكن بنجاح (ID: {resident_id})")
    
    # 3. تحديث معلومات الساكن
    print("\n3. اختبار تحديث معلومات الساكن...")
    update_data = {
        'name': 'اختبار ساكن محدث',
        'phone': '0502222222',
        'email': 'test_updated@test.com',
        'unit_id': test_resident['unit_id'],
        'status': 'نشط'
    }
    result = update_resident(resident_id, update_data)
    assert result['success'], f"فشل في تحديث الساكن: {result.get('error')}"
    print(f"   ✓ تم تحديث معلومات الساكن بنجاح")
    
    # 4. إخراج الساكن
    print("\n4. اختبار إخراج الساكن...")
    result = checkout_resident(resident_id)
    assert result['success'], f"فشل في إخراج الساكن: {result.get('error')}"
    print(f"   ✓ تم إخراج الساكن بنجاح")
    
    # 5. حذف الساكن
    print("\n5. اختبار حذف الساكن...")
    result = delete_resident(resident_id)
    assert result['success'], f"فشل في حذف الساكن: {result.get('error')}"
    print(f"   ✓ تم حذف الساكن بنجاح")
    
    print("\n" + "="*50)
    print("✓ جميع الاختبارات تمت بنجاح!")
    print("="*50)


if __name__ == '__main__':
    test_resident_lifecycle()
