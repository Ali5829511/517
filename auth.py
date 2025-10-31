#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المصادقة والتفويض
Authentication and Authorization System
"""

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    jsonify,
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
from database_api import get_db_connection
import logging

logger = logging.getLogger(__name__)

# إنشاء Blueprint للمصادقة / Create authentication Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(f):
    """
    ديكورتر للتحقق من تسجيل الدخول
    Decorator to check if user is logged in
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """
    ديكورتر للتحقق من صلاحيات المدير
    Decorator to check if user has admin privileges
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        if session.get("role") != "admin":
            flash("ليس لديك صلاحية الوصول لهذه الصفحة", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


def check_login_attempts(username, ip_address):
    """
    التحقق من محاولات تسجيل الدخول
    Check login attempts to prevent brute force
    """
    try:
        conn = get_db_connection()
        fifteen_min_ago = datetime.now() - timedelta(minutes=15)

        # عد المحاولات الفاشلة في آخر 15 دقيقة
        # Count failed attempts in last 15 minutes
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) as count FROM login_attempts 
            WHERE username = ? AND ip_address = ? 
            AND timestamp > ? AND success = 0
        """,
            (username, ip_address, fifteen_min_ago),
        )
        result = cursor.fetchone()
        conn.close()

        count = result["count"] if result else 0
        return count < 5  # السماح بـ 5 محاولات فقط / Allow only 5 attempts

    except Exception as e:
        logger.error(f"Error checking login attempts: {e}")
        return True  # السماح بالمحاولة في حالة الخطأ / Allow attempt on error


def log_login_attempt(username, ip_address, success):
    """
    تسجيل محاولة تسجيل الدخول
    Log login attempt
    """
    try:
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO login_attempts (username, ip_address, success)
            VALUES (?, ?, ?)
        """,
            (username, ip_address, success),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error logging login attempt: {e}")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    صفحة تسجيل الدخول
    Login page
    """
    # إذا كان المستخدم مسجل دخول بالفعل، إعادة توجيهه للصفحة الرئيسية
    # If user is already logged in, redirect to main page
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        ip_address = request.remote_addr

        # التحقق من المدخلات / Validate inputs
        if not username or not password:
            flash("يرجى إدخال اسم المستخدم وكلمة المرور", "danger")
            return render_template("login.html")

        # التحقق من محاولات تسجيل الدخول / Check login attempts
        if not check_login_attempts(username, ip_address):
            flash(
                "تم تجاوز عدد محاولات تسجيل الدخول. يرجى المحاولة بعد 15 دقيقة",
                "danger",
            )
            log_login_attempt(username, ip_address, False)
            return render_template("login.html")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND is_active = 1",
                (username,),
            )
            user = cursor.fetchone()

            if user and check_password_hash(user["password_hash"], password):
                # تسجيل دخول ناجح / Successful login
                session.clear()
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                session["full_name"] = user["full_name"] or user["username"]
                session.permanent = True

                # تحديث آخر تسجيل دخول / Update last login
                conn.execute(
                    "UPDATE users SET last_login = ? WHERE id = ?",
                    (datetime.now(), user["id"]),
                )
                conn.commit()

                log_login_attempt(username, ip_address, True)
                flash(f"مرحباً {session['full_name']}", "success")
                conn.close()

                # إعادة التوجيه للصفحة المطلوبة أو الصفحة الرئيسية
                # Redirect to requested page or main page
                next_page = request.args.get("next")
                return redirect(next_page if next_page else url_for("index"))
            else:
                # فشل تسجيل الدخول / Failed login
                log_login_attempt(username, ip_address, False)
                flash("اسم المستخدم أو كلمة المرور غير صحيحة", "danger")
                conn.close()

        except Exception as e:
            logger.error(f"Login error: {e}")
            flash("حدث خطأ أثناء تسجيل الدخول", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """
    تسجيل الخروج
    Logout
    """
    username = session.get("username", "مستخدم")
    session.clear()
    flash(f"تم تسجيل خروج {username} بنجاح", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    صفحة التسجيل
    Registration page
    """
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        full_name = request.form.get("full_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # التحقق من المدخلات / Validate inputs
        if not all([username, email, password, confirm_password]):
            flash("يرجى ملء جميع الحقول", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("كلمات المرور غير متطابقة", "danger")
            return render_template("register.html")

        if len(password) < 8:
            flash("يجب أن تكون كلمة المرور 8 أحرف على الأقل", "danger")
            return render_template("register.html")

        try:
            password_hash = generate_password_hash(password)
            conn = get_db_connection()

            conn.execute(
                """
                INSERT INTO users (username, email, password_hash, role, full_name)
                VALUES (?, ?, ?, ?, ?)
            """,
                (username, email, password_hash, "user", full_name),
            )
            conn.commit()
            conn.close()

            flash("تم إنشاء الحساب بنجاح. يمكنك تسجيل الدخول الآن", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            logger.error(f"Registration error: {e}")
            flash("اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل", "danger")

    return render_template("register.html")


@auth_bp.route("/profile")
@login_required
def profile():
    """
    صفحة الملف الشخصي
    User profile page
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
        user = cursor.fetchone()
        conn.close()

        return render_template("profile.html", user=user)
    except Exception as e:
        logger.error(f"Profile error: {e}")
        flash("حدث خطأ أثناء تحميل الملف الشخصي", "danger")
        return redirect(url_for("index"))


@auth_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    """
    تغيير كلمة المرور
    Change password
    """
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if not all([current_password, new_password, confirm_password]):
        flash("يرجى ملء جميع الحقول", "danger")
        return redirect(url_for("auth.profile"))

    if new_password != confirm_password:
        flash("كلمات المرور الجديدة غير متطابقة", "danger")
        return redirect(url_for("auth.profile"))

    if len(new_password) < 8:
        flash("يجب أن تكون كلمة المرور 8 أحرف على الأقل", "danger")
        return redirect(url_for("auth.profile"))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
        user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], current_password):
            new_password_hash = generate_password_hash(new_password)
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (new_password_hash, session["user_id"]),
            )
            conn.commit()
            conn.close()
            flash("تم تغيير كلمة المرور بنجاح", "success")
        else:
            conn.close()
            flash("كلمة المرور الحالية غير صحيحة", "danger")

    except Exception as e:
        logger.error(f"Change password error: {e}")
        flash("حدث خطأ أثناء تغيير كلمة المرور", "danger")

    return redirect(url_for("auth.profile"))
