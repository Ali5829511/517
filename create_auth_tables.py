#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء جداول المصادقة في قاعدة البيانات
Create authentication tables in database
"""

import sqlite3
from werkzeug.security import generate_password_hash

def create_auth_tables():
    """إنشاء جداول المستخدمين ومحاولات تسجيل الدخول"""
    conn = sqlite3.connect('housing_database.db')
    cursor = conn.cursor()
    
    # إنشاء جدول المستخدمين
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT 1
    )
    ''')
    
    # إنشاء جدول محاولات تسجيل الدخول
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        ip_address TEXT,
        success BOOLEAN,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # إضافة مستخدم افتراضي (admin)
    admin_password = generate_password_hash('Admin@2025')
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@imamu.edu.sa', admin_password, 'admin'))
        print("✅ تم إنشاء المستخدم الافتراضي:")
        print("   اسم المستخدم: admin")
        print("   كلمة المرور: Admin@2025")
        print("   ⚠️ يرجى تغيير كلمة المرور بعد أول تسجيل دخول!")
    except sqlite3.IntegrityError:
        print("✓ المستخدم الافتراضي موجود بالفعل")
    
    conn.commit()
    conn.close()
    print("✅ تم إنشاء جداول المصادقة بنجاح")

if __name__ == '__main__':
    create_auth_tables()
