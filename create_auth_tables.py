#!/usr/bin/env python3
"""
Script to create authentication tables in the housing database
"""
import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_auth_tables():
    """Create users and login_attempts tables"""
    conn = sqlite3.connect('housing_database.db')
    cursor = conn.cursor()
    
    # Create users table
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
    
    # Create login_attempts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        ip_address TEXT,
        success BOOLEAN,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    print("✅ Authentication tables created successfully")
    
    # Check if admin user already exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    admin_exists = cursor.fetchone()[0] > 0
    
    if not admin_exists:
        # Create default admin user
        admin_password_hash = generate_password_hash('Admin@2025')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@imamu.edu.sa', admin_password_hash, 'admin', 1))
        conn.commit()
        print("\n✅ Default admin user created:")
        print("   Username: admin")
        print("   Password: Admin@2025")
        print("   ⚠️  Please change the password after first login!")
    else:
        print("\n✅ Admin user already exists")
    
    # Display table information
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"\n📊 Total users in database: {user_count}")
    
    conn.close()

if __name__ == '__main__':
    create_auth_tables()
