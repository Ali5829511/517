"""
Authentication database operations module
Handles user authentication, login attempts, and password resets
"""
import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = 'housing_database.db'

def get_db_connection():
    """Get a database connection with row factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND is_active = 1',
        (username,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE email = ? AND is_active = 1',
        (email,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None

def create_user(username, email, password, role='user', name=None):
    """Create a new user"""
    conn = get_db_connection()
    try:
        password_hash = generate_password_hash(password)
        cursor = conn.execute('''
            INSERT INTO users (username, email, password_hash, role, name)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, role, name))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {'success': True, 'user_id': user_id}
    except sqlite3.IntegrityError as e:
        conn.close()
        return {'success': False, 'error': str(e)}

def update_user_password(username, new_password):
    """Update user password"""
    conn = get_db_connection()
    password_hash = generate_password_hash(new_password)
    conn.execute(
        'UPDATE users SET password_hash = ? WHERE username = ?',
        (password_hash, username)
    )
    conn.commit()
    conn.close()
    return True

def update_last_login(username):
    """Update user's last login timestamp"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE users SET last_login = ? WHERE username = ?',
        (datetime.now(), username)
    )
    conn.commit()
    conn.close()

def verify_password(user, password):
    """Verify user password"""
    if not user or 'password_hash' not in user:
        return False
    return check_password_hash(user['password_hash'], password)

def check_login_attempts(username, ip_address, max_attempts=5, window_minutes=15):
    """
    Check if user has exceeded login attempts
    Returns True if user can attempt login, False if locked out
    """
    conn = get_db_connection()
    cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
    
    attempts = conn.execute('''
        SELECT COUNT(*) as count FROM login_attempts
        WHERE username = ? AND ip_address = ?
        AND timestamp > ? AND success = 0
    ''', (username, ip_address, cutoff_time)).fetchone()
    
    conn.close()
    return attempts['count'] < max_attempts

def log_login_attempt(username, ip_address, success):
    """Log a login attempt"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO login_attempts (username, ip_address, success, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (username, ip_address, success, datetime.now()))
    conn.commit()
    conn.close()

def get_all_users():
    """Get all users (for admin panel)"""
    conn = get_db_connection()
    users = conn.execute('''
        SELECT id, username, email, role, name, created_at, last_login, is_active
        FROM users
        ORDER BY created_at DESC
    ''').fetchall()
    conn.close()
    return [dict(user) for user in users]

def delete_user(username):
    """Delete a user (soft delete by setting is_active to 0)"""
    if username == 'admin':
        return {'success': False, 'error': 'Cannot delete admin user'}
    
    conn = get_db_connection()
    conn.execute('UPDATE users SET is_active = 0 WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    return {'success': True}

def user_exists(username=None, email=None):
    """Check if user exists by username or email"""
    conn = get_db_connection()
    
    if username:
        count = conn.execute(
            'SELECT COUNT(*) as count FROM users WHERE username = ?',
            (username,)
        ).fetchone()['count']
        if count > 0:
            conn.close()
            return True
    
    if email:
        count = conn.execute(
            'SELECT COUNT(*) as count FROM users WHERE email = ?',
            (email,)
        ).fetchone()['count']
        if count > 0:
            conn.close()
            return True
    
    conn.close()
    return False
