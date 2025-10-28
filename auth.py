"""
Authentication module for Housing Management System
Provides secure login, registration, and session management
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# Database connection helper
def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect('housing_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorator
def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('يرجى تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('يرجى تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('غير مصرح لك بالوصول لهذه الصفحة', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def check_login_attempts(username, ip_address):
    """Check if user has exceeded login attempts"""
    conn = get_db_connection()
    fifteen_min_ago = datetime.now() - timedelta(minutes=15)
    
    # Count failed attempts in last 15 minutes
    attempts = conn.execute('''
        SELECT COUNT(*) as count FROM login_attempts 
        WHERE username = ? AND ip_address = ? 
        AND timestamp > ? AND success = 0
    ''', (username, ip_address, fifteen_min_ago.isoformat())).fetchone()
    
    conn.close()
    return attempts['count'] < 5

def log_login_attempt(username, ip_address, success):
    """Log a login attempt"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO login_attempts (username, ip_address, success)
        VALUES (?, ?, ?)
    ''', (username, ip_address, success))
    conn.commit()
    conn.close()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip_address = request.remote_addr
        
        # Check login attempts
        if not check_login_attempts(username, ip_address):
            flash('تم تجاوز عدد محاولات تسجيل الدخول. يرجى المحاولة بعد 15 دقيقة', 'danger')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND is_active = 1', 
            (username,)
        ).fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            # Successful login
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['email'] = user['email']
            session.permanent = True
            
            # Update last login
            conn.execute(
                'UPDATE users SET last_login = ? WHERE id = ?', 
                (datetime.now().isoformat(), user['id'])
            )
            conn.commit()
            
            log_login_attempt(username, ip_address, True)
            flash('تم تسجيل الدخول بنجاح', 'success')
            conn.close()
            
            # Redirect to home page
            return redirect(url_for('index'))
        else:
            # Failed login
            log_login_attempt(username, ip_address, False)
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
            conn.close()
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Logout handler"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and handler"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('كلمات المرور غير متطابقة', 'danger')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('يجب أن تكون كلمة المرور 8 أحرف على الأقل', 'danger')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, 'user'))
            conn.commit()
            flash('تم إنشاء الحساب بنجاح. يمكنك تسجيل الدخول الآن', 'success')
            conn.close()
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل', 'danger')
            conn.close()
    
    return render_template('register.html')

@auth_bp.route('/api/check-auth')
def check_auth():
    """API endpoint to check authentication status"""
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'username': session.get('username'),
            'role': session.get('role')
        })
    else:
        return jsonify({'authenticated': False}), 401
