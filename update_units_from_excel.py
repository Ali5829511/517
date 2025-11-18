#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لتحديث بيانات الفلل والوحدات السكنية من ملف Excel
Update villas and residential units data from Excel file
"""

import sqlite3
import pandas as pd
import sys
from datetime import datetime


def backup_database(db_path):
    """
    إنشاء نسخة احتياطية من قاعدة البيانات
    Create a backup of the database
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{db_path}.backup_{timestamp}"
    
    try:
        conn = sqlite3.connect(db_path)
        backup_conn = sqlite3.connect(backup_path)
        conn.backup(backup_conn)
        backup_conn.close()
        conn.close()
        print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ فشل إنشاء النسخة الاحتياطية: {e}")
        return None


def get_current_data(conn):
    """
    جلب البيانات الحالية من قاعدة البيانات
    Fetch current data from database
    """
    cursor = conn.cursor()
    
    # Get current buildings with their units and residents
    cursor.execute("""
        SELECT 
            b.id, b.building_number, b.building_type,
            u.id as unit_id, u.unit_number, u.unit_type, u.status,
            r.id as resident_id, r.name, r.unit_id as resident_unit_id
        FROM buildings b
        LEFT JOIN units u ON b.id = u.building_id
        LEFT JOIN residents r ON u.id = r.unit_id
        ORDER BY b.id, u.id
    """)
    
    return cursor.fetchall()


def update_from_excel(excel_path, db_path, dry_run=False):
    """
    تحديث قاعدة البيانات من ملف Excel
    Update database from Excel file
    
    Args:
        excel_path: مسار ملف Excel
        db_path: مسار قاعدة البيانات
        dry_run: إذا كان True، لن يتم حفظ التغييرات
    """
    print("=" * 60)
    print("تحديث بيانات الفلل والوحدات السكنية من Excel")
    print("Update Villas and Residential Units from Excel")
    print("=" * 60)
    
    # Read Excel file
    try:
        df = pd.read_excel(excel_path)
        print(f"\n✅ تم قراءة ملف Excel: {len(df)} سجل")
    except Exception as e:
        print(f"❌ خطأ في قراءة ملف Excel: {e}")
        return False
    
    # Validate columns
    required_cols = ['اسم الوحدة', 'الوصف', 'رقم فلة / عمارة ', 'رقم الشقة']
    if not all(col in df.columns for col in required_cols):
        print(f"❌ الأعمدة المطلوبة غير موجودة في ملف Excel")
        print(f"   الأعمدة الموجودة: {list(df.columns)}")
        return False
    
    # Create backup
    if not dry_run:
        backup_path = backup_database(db_path)
        if not backup_path:
            print("❌ فشل إنشاء النسخة الاحتياطية، التوقف...")
            return False
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = OFF")  # Temporarily disable foreign keys
    cursor = conn.cursor()
    
    try:
        # Step 1: Clear existing buildings and units
        print("\n📋 الخطوة 1: حذف البيانات القديمة...")
        
        # Store resident associations before clearing
        cursor.execute("""
            SELECT r.id, r.name, r.national_id, b.building_number, u.unit_number
            FROM residents r
            JOIN units u ON r.unit_id = u.id
            JOIN buildings b ON u.building_id = b.id
        """)
        resident_associations = cursor.fetchall()
        print(f"   تم حفظ {len(resident_associations)} ارتباط للسكان")
        
        # Clear units and buildings
        cursor.execute("DELETE FROM units")
        cursor.execute("DELETE FROM buildings")
        
        if not dry_run:
            conn.commit()
        
        print("   ✅ تم حذف البيانات القديمة")
        
        # Step 2: Process villas
        print("\n📋 الخطوة 2: إضافة الفلل...")
        villas = df[df['الوصف'] == 'منطفة الفلل'].copy()
        villa_count = 0
        
        for _, row in villas.iterrows():
            building_num = int(row['رقم فلة / عمارة '])
            building_name = f"فيلا {building_num}"
            
            # Insert building
            cursor.execute("""
                INSERT INTO buildings (building_number, building_type, total_units, occupied_units, status)
                VALUES (?, ?, ?, ?, ?)
            """, (building_name, 'فيلا', 1, 0, 'نشط'))
            
            building_id = cursor.lastrowid
            
            # Insert unit
            cursor.execute("""
                INSERT INTO units (building_id, unit_number, unit_type, status)
                VALUES (?, ?, ?, ?)
            """, (building_id, '1', 'فيلا', 'شاغر'))
            
            villa_count += 1
        
        print(f"   ✅ تم إضافة {villa_count} فيلا")
        
        # Step 3: Process apartment buildings
        print("\n📋 الخطوة 3: إضافة العمارات والشقق...")
        apartments = df[df['الوصف'].str.contains('المباني', na=False)].copy()
        
        # Group by building number
        buildings_dict = {}
        for _, row in apartments.iterrows():
            building_num = int(row['رقم فلة / عمارة '])
            unit_num = int(row['رقم الشقة'])
            
            if building_num not in buildings_dict:
                buildings_dict[building_num] = []
            
            buildings_dict[building_num].append(unit_num)
        
        building_count = 0
        apartment_count = 0
        
        for building_num in sorted(buildings_dict.keys()):
            building_name = f"عمارة {building_num}"
            units = sorted(set(buildings_dict[building_num]))  # Remove duplicates
            total_units = len(units)
            
            # Insert building
            cursor.execute("""
                INSERT INTO buildings (building_number, building_type, total_units, occupied_units, status)
                VALUES (?, ?, ?, ?, ?)
            """, (building_name, 'عمارة', total_units, 0, 'نشط'))
            
            building_id = cursor.lastrowid
            building_count += 1
            
            # Insert units
            for unit_num in units:
                cursor.execute("""
                    INSERT INTO units (building_id, unit_number, unit_type, status)
                    VALUES (?, ?, ?, ?)
                """, (building_id, str(unit_num), 'شقة', 'شاغر'))
                apartment_count += 1
        
        print(f"   ✅ تم إضافة {building_count} عمارة")
        print(f"   ✅ تم إضافة {apartment_count} شقة")
        
        # Step 4: Restore resident associations
        print("\n📋 الخطوة 4: استعادة ارتباطات السكان...")
        restored_count = 0
        not_found_count = 0
        orphaned_residents = []
        
        for res_id, res_name, nat_id, building_name, unit_num in resident_associations:
            # Find the new unit_id
            cursor.execute("""
                SELECT u.id 
                FROM units u
                JOIN buildings b ON u.building_id = b.id
                WHERE b.building_number = ? AND u.unit_number = ?
            """, (building_name, unit_num))
            
            result = cursor.fetchone()
            if result:
                new_unit_id = result[0]
                
                # Update resident
                cursor.execute("""
                    UPDATE residents 
                    SET unit_id = ?
                    WHERE id = ?
                """, (new_unit_id, res_id))
                
                # Update unit status
                cursor.execute("""
                    UPDATE units 
                    SET status = 'مشغول'
                    WHERE id = ?
                """, (new_unit_id,))
                
                restored_count += 1
            else:
                # Resident's unit no longer exists - set unit_id to NULL
                cursor.execute("""
                    UPDATE residents 
                    SET unit_id = NULL, status = 'غير نشط'
                    WHERE id = ?
                """, (res_id,))
                orphaned_residents.append((res_name, building_name, unit_num))
                not_found_count += 1
        
        print(f"   ✅ تم استعادة {restored_count} ارتباط من أصل {len(resident_associations)}")
        if not_found_count > 0:
            print(f"   ⚠️  {not_found_count} ساكن لم يتم العثور على وحداتهم (تم تعيينهم كغير نشط)")
            if not_found_count <= 10:
                print("   السكان المتأثرون:")
                for name, building, unit in orphaned_residents:
                    print(f"      - {name} ({building} - {unit})")
        
        # Step 5: Update occupied_units count in buildings
        print("\n📋 الخطوة 5: تحديث عدد الوحدات المشغولة...")
        cursor.execute("""
            UPDATE buildings 
            SET occupied_units = (
                SELECT COUNT(*) 
                FROM units 
                WHERE building_id = buildings.id AND status = 'مشغول'
            )
        """)
        
        # Commit changes
        if not dry_run:
            conn.commit()
            print("\n✅ تم حفظ جميع التغييرات")
        else:
            conn.rollback()
            print("\n⚠️  وضع الاختبار (dry run) - لم يتم حفظ التغييرات")
        
        # Step 6: Display statistics
        print("\n" + "=" * 60)
        print("📊 الإحصائيات النهائية / Final Statistics")
        print("=" * 60)
        
        cursor.execute("SELECT COUNT(*) FROM buildings WHERE building_type = 'فيلا'")
        print(f"إجمالي الفلل: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM buildings WHERE building_type = 'عمارة'")
        print(f"إجمالي العمارات: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM units WHERE unit_type = 'فيلا'")
        print(f"إجمالي وحدات الفلل: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM units WHERE unit_type = 'شقة'")
        print(f"إجمالي الشقق: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM units WHERE status = 'مشغول'")
        print(f"الوحدات المشغولة: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM units WHERE status = 'شاغر'")
        print(f"الوحدات الشاغرة: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM residents WHERE unit_id IS NOT NULL")
        print(f"السكان المرتبطون بوحدات: {cursor.fetchone()[0]}")
        
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في التحديث: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.execute("PRAGMA foreign_keys = ON")  # Re-enable foreign keys
        conn.close()


if __name__ == "__main__":
    excel_file = "الوحدات السكنية.xlsx"
    database_file = "housing_database.db"
    
    # Check for dry-run flag
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    if dry_run:
        print("🔍 وضع الاختبار (Dry Run Mode) - لن يتم حفظ التغييرات\n")
    
    success = update_from_excel(excel_file, database_file, dry_run=dry_run)
    
    if success:
        print("\n✅ تمت العملية بنجاح!")
        sys.exit(0)
    else:
        print("\n❌ فشلت العملية!")
        sys.exit(1)
