#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبارات لتحديث بيانات الفلل والوحدات السكنية
Tests for villas and residential units update
"""

import sqlite3
import pandas as pd


def test_excel_file_exists():
    """Test that the Excel file exists and is readable"""
    try:
        df = pd.read_excel('الوحدات السكنية.xlsx')
        assert len(df) > 0, "Excel file is empty"
        print("✅ Excel file exists and is readable")
        return True
    except Exception as e:
        print(f"❌ Excel file error: {e}")
        return False


def test_database_exists():
    """Test that the database exists and is accessible"""
    try:
        conn = sqlite3.connect('housing_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM buildings")
        count = cursor.fetchone()[0]
        conn.close()
        assert count > 0, "Database has no buildings"
        print("✅ Database exists and is accessible")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def test_villa_count():
    """Test that villa count matches Excel"""
    try:
        # Excel data
        df = pd.read_excel('الوحدات السكنية.xlsx')
        excel_villas = len(df[df['الوصف'] == 'منطفة الفلل'])
        
        # Database data
        conn = sqlite3.connect('housing_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM buildings WHERE building_type = 'فيلا'")
        db_villas = cursor.fetchone()[0]
        conn.close()
        
        assert excel_villas == db_villas, f"Villa count mismatch: Excel={excel_villas}, DB={db_villas}"
        print(f"✅ Villa count matches: {db_villas}")
        return True
    except Exception as e:
        print(f"❌ Villa count test failed: {e}")
        return False


def test_apartment_building_count():
    """Test that apartment building count matches Excel"""
    try:
        # Excel data
        df = pd.read_excel('الوحدات السكنية.xlsx')
        apartments = df[df['الوصف'].str.contains('المباني', na=False)]
        excel_buildings = len(apartments['رقم فلة / عمارة '].unique())
        
        # Database data
        conn = sqlite3.connect('housing_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM buildings WHERE building_type = 'عمارة'")
        db_buildings = cursor.fetchone()[0]
        conn.close()
        
        assert excel_buildings == db_buildings, f"Building count mismatch: Excel={excel_buildings}, DB={db_buildings}"
        print(f"✅ Apartment building count matches: {db_buildings}")
        return True
    except Exception as e:
        print(f"❌ Apartment building count test failed: {e}")
        return False


def test_unit_numbering():
    """Test that unit numbering follows the Excel pattern"""
    try:
        conn = sqlite3.connect('housing_database.db')
        cursor = conn.cursor()
        
        # Get units for building 1
        cursor.execute("""
            SELECT u.unit_number
            FROM units u
            JOIN buildings b ON u.building_id = b.id
            WHERE b.building_number = 'عمارة 1'
            ORDER BY CAST(u.unit_number AS INTEGER)
        """)
        
        unit_numbers = [int(row[0]) for row in cursor.fetchall()]
        conn.close()
        
        # Expected pattern: 1-4, 11-14, 21-24, 31-34, 41-44
        expected = [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44]
        
        assert unit_numbers == expected, f"Unit numbering doesn't match expected pattern"
        print(f"✅ Unit numbering follows correct pattern")
        return True
    except Exception as e:
        print(f"❌ Unit numbering test failed: {e}")
        return False


def test_new_buildings_exist():
    """Test that new buildings (72-79) exist in database"""
    try:
        conn = sqlite3.connect('housing_database.db')
        cursor = conn.cursor()
        
        new_buildings = [72, 73, 74, 75, 76, 77, 78, 79]
        missing = []
        
        for bnum in new_buildings:
            cursor.execute("""
                SELECT COUNT(*) FROM buildings 
                WHERE building_number = ?
            """, (f'عمارة {bnum}',))
            
            if cursor.fetchone()[0] == 0:
                missing.append(bnum)
        
        conn.close()
        
        assert len(missing) == 0, f"Missing buildings: {missing}"
        print(f"✅ All new buildings (72-79) exist")
        return True
    except Exception as e:
        print(f"❌ New buildings test failed: {e}")
        return False


def test_foreign_key_integrity():
    """Test foreign key integrity"""
    try:
        conn = sqlite3.connect('housing_database.db')
        cursor = conn.cursor()
        
        # Check for orphaned units
        cursor.execute("""
            SELECT COUNT(*) FROM units 
            WHERE building_id NOT IN (SELECT id FROM buildings)
        """)
        orphaned_units = cursor.fetchone()[0]
        
        # Check for orphaned residents
        cursor.execute("""
            SELECT COUNT(*) FROM residents 
            WHERE unit_id IS NOT NULL 
            AND unit_id NOT IN (SELECT id FROM units)
        """)
        orphaned_residents = cursor.fetchone()[0]
        
        conn.close()
        
        assert orphaned_units == 0, f"Found {orphaned_units} orphaned units"
        assert orphaned_residents == 0, f"Found {orphaned_residents} orphaned residents"
        print(f"✅ Foreign key integrity maintained")
        return True
    except Exception as e:
        print(f"❌ Foreign key integrity test failed: {e}")
        return False


def test_backup_exists():
    """Test that backup was created"""
    import os
    import glob
    
    try:
        backups = glob.glob('housing_database.db.backup_*')
        assert len(backups) > 0, "No backup files found"
        print(f"✅ Backup exists: {len(backups)} backup file(s) found")
        return True
    except Exception as e:
        print(f"❌ Backup test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("تشغيل اختبارات تحديث البيانات")
    print("Running Data Update Tests")
    print("=" * 70)
    print()
    
    tests = [
        test_excel_file_exists,
        test_database_exists,
        test_villa_count,
        test_apartment_building_count,
        test_unit_numbering,
        test_new_buildings_exist,
        test_foreign_key_integrity,
        test_backup_exists,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"النتائج / Results: {passed} نجح ✅, {failed} فشل ❌")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
