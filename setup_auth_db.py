#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعداد قاعدة بيانات نظام المصادقة
Setup authentication database tables
"""

import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime


def setup_auth_tables():
    """إنشاء جداول المصادقة / Create authentication tables"""
    conn = sqlite3.connect("housing_database.db")
    cursor = conn.cursor()

    # جدول المستخدمين / Users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'user',
        full_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT 1
    )
    """
    )

    # جدول محاولات تسجيل الدخول / Login attempts table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        ip_address TEXT,
        success BOOLEAN,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    # إنشاء فهارس لتحسين الأداء / Create indexes for performance
    cursor.execute(
        """
    CREATE INDEX IF NOT EXISTS idx_username 
    ON users(username)
    """
    )

    cursor.execute(
        """
    CREATE INDEX IF NOT EXISTS idx_login_attempts_username 
    ON login_attempts(username, timestamp)
    """
    )

    conn.commit()
    print("✅ تم إنشاء جداول المصادقة بنجاح / Authentication tables created successfully")

    # إنشاء مستخدم المدير الافتراضي / Create default admin user
    try:
        admin_password_hash = generate_password_hash("Admin@2025")
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, role, full_name)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("admin", "admin@imamu.edu.sa", admin_password_hash, "admin", "مدير النظام"),
        )
        conn.commit()
        print("\n✅ تم إنشاء مستخدم المدير الافتراضي / Default admin user created:")
        print("   اسم المستخدم / Username: admin")
        print("   كلمة المرور / Password: Admin@2025")
        print("   ⚠️  يرجى تغيير كلمة المرور بعد أول تسجيل دخول!")
        print("   ⚠️  Please change the password after first login!")
    except sqlite3.IntegrityError:
        print("\n⚠️  مستخدم المدير موجود بالفعل / Admin user already exists")

    conn.close()


if __name__ == "__main__":
    setup_auth_tables()
