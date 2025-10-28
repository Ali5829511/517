"""
Tests for authentication system
"""
import pytest
import sqlite3
from app import app, get_db_connection
from werkzeug.security import check_password_hash


def test_auth_tables_exist():
    """Test that authentication tables exist in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check users table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert cursor.fetchone() is not None
    
    # Check login_attempts table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='login_attempts'")
    assert cursor.fetchone() is not None
    
    conn.close()


def test_admin_user_exists():
    """Test that admin user exists in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    assert admin is not None
    assert admin['username'] == 'admin'
    assert admin['role'] == 'admin'
    assert admin['is_active'] == 1
    
    conn.close()


def test_admin_password():
    """Test that admin password is correctly hashed"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password_hash FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    assert admin is not None
    # Verify the password hash works
    assert check_password_hash(admin['password_hash'], 'Admin@2025')
    
    conn.close()


def test_login_endpoint_exists():
    """Test that login API endpoint exists"""
    client = app.test_client()
    response = client.post('/api/login', json={})
    # Should return 400 (bad request) not 404 (not found)
    assert response.status_code in [400, 401, 500]


def test_logout_endpoint_exists():
    """Test that logout API endpoint exists"""
    client = app.test_client()
    response = client.post('/api/logout')
    assert response.status_code == 200


def test_get_db_connection():
    """Test database connection helper"""
    conn = get_db_connection()
    assert conn is not None
    
    # Test that row_factory is set
    cursor = conn.cursor()
    cursor.execute("SELECT 1 as test")
    row = cursor.fetchone()
    assert row['test'] == 1
    
    conn.close()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
