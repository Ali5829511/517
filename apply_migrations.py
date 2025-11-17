#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لتطبيق التغييرات على قاعدة البيانات
Apply database migrations for vehicles and violations
"""

import sqlite3
import os
import sys

DATABASE = "housing_database.db"

def apply_migration(migration_file):
    """تطبيق ملف migration على قاعدة البيانات"""
    print(f"تطبيق التغييرات من: {migration_file}")
    
    try:
        # قراءة ملف SQL
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # تفعيل المفاتيح الأجنبية
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # تنفيذ السكريبت
        cursor.executescript(sql_script)
        
        conn.commit()
        conn.close()
        
        print(f"✅ تم تطبيق التغييرات بنجاح من: {migration_file}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تطبيق التغييرات: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("تطبيق التغييرات على قاعدة البيانات")
    print("Apply Database Migrations")
    print("=" * 60)
    
    # التحقق من وجود قاعدة البيانات
    if not os.path.exists(DATABASE):
        print(f"❌ قاعدة البيانات غير موجودة: {DATABASE}")
        sys.exit(1)
    
    # تطبيق التغييرات
    migrations_dir = "migrations"
    if not os.path.exists(migrations_dir):
        print(f"❌ مجلد التغييرات غير موجود: {migrations_dir}")
        sys.exit(1)
    
    # تطبيق كل ملف SQL في المجلد
    migration_files = sorted([
        f for f in os.listdir(migrations_dir)
        if f.endswith('.sql')
    ])
    
    if not migration_files:
        print("⚠️  لا توجد ملفات تغييرات للتطبيق")
        sys.exit(0)
    
    success_count = 0
    for migration_file in migration_files:
        file_path = os.path.join(migrations_dir, migration_file)
        if apply_migration(file_path):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"تم تطبيق {success_count} من {len(migration_files)} تغيير بنجاح")
    print("=" * 60)
    
    # عرض الجداول الجديدة
    print("\nالجداول الموجودة في قاعدة البيانات:")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    for table in tables:
        print(f"  - {table[0]}")
    conn.close()

if __name__ == "__main__":
    main()
