#!/usr/bin/env python3
"""
Database migration script to add users and login_attempts tables
"""
import sqlite3
from werkzeug.security import generate_password_hash

def migrate_database():
    """Create users and login_attempts tables in the database"""
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
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create login_attempts table for security
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            ip_address TEXT,
            success BOOLEAN,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if admin user exists
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
    if cursor.fetchone()[0] == 0:
        # Insert default admin user
        admin_password_hash = generate_password_hash('Admin@2025')
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, role, name, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', admin_password_hash, 'aliayashi517@gmail.com', 'admin', 'مدير النظام', 1))
        print("✓ Default admin user created")
    else:
        print("✓ Admin user already exists")
    
    conn.commit()
    conn.close()
    
    print("✓ Database migration completed successfully")
    print("✓ Tables created: users, login_attempts")

if __name__ == '__main__':
    migrate_database()
