# -*- coding: utf-8 -*-
"""
نظام المصادقة - Authentication System
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

def get_db_connection():
    """الاتصال بقاعدة البيانات"""
    conn = sqlite3.connect('housing_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """التحقق من تسجيل الدخول"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('يرجى تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def check_login_attempts(username, ip_address):
    """التحقق من محاولات تسجيل الدخول"""
    conn = get_db_connection()
    fifteen_min_ago = datetime.now() - timedelta(minutes=15)
    attempts = conn.execute('''
        SELECT COUNT(*) as count FROM login_attempts 
        WHERE username = ? AND ip_address = ? 
        AND timestamp > ? AND success = 0
    ''', (username, ip_address, fifteen_min_ago)).fetchone()
    conn.close()
    return attempts['count'] < 5

def log_login_attempt(username, ip_address, success):
    """تسجيل محاولة تسجيل الدخول"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO login_attempts (username, ip_address, success)
        VALUES (?, ?, ?)
    ''', (username, ip_address, success))
    conn.commit()
    conn.close()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip_address = request.remote_addr
        
        if not check_login_attempts(username, ip_address):
            flash('تم تجاوز عدد محاولات تسجيل الدخول. يرجى المحاولة بعد 15 دقيقة', 'danger')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', 
                           (username,)).fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session.permanent = True
            
            conn.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                        (datetime.now(), user['id']))
            conn.commit()
            
            log_login_attempt(username, ip_address, True)
            flash('تم تسجيل الدخول بنجاح', 'success')
            conn.close()
            return redirect('/main_portal.html')
        else:
            log_login_attempt(username, ip_address, False)
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
            conn.close()
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """صفحة التسجيل"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
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
