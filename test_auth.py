#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبارات نظام المصادقة
Authentication system tests
"""

import pytest
import sqlite3
from werkzeug.security import check_password_hash
from database_api import get_db_connection


def test_auth_tables_exist():
    """Test that authentication tables exist"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check users table
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
    )
    assert cursor.fetchone() is not None, "Users table should exist"

    # Check login_attempts table
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='login_attempts'"
    )
    assert cursor.fetchone() is not None, "Login attempts table should exist"

    conn.close()


def test_admin_user_exists():
    """Test that admin user was created"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username='admin'")
    admin = cursor.fetchone()

    assert admin is not None, "Admin user should exist"
    assert admin["username"] == "admin"
    assert admin["email"] == "admin@imamu.edu.sa"
    assert admin["role"] == "admin"
    assert admin["is_active"] == 1

    conn.close()


def test_admin_password():
    """Test that admin password is correct"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username='admin'")
    result = cursor.fetchone()

    assert result is not None, "Admin user should exist"
    assert check_password_hash(
        result["password_hash"], "Admin@2025"
    ), "Admin password should be 'Admin@2025'"

    conn.close()


def test_auth_blueprint_imported():
    """Test that auth blueprint is imported"""
    from app import app

    # Check that auth blueprint is registered
    blueprints = [bp.name for bp in app.blueprints.values()]
    assert "auth" in blueprints, "Auth blueprint should be registered"


def test_auth_routes_exist():
    """Test that auth routes are registered"""
    from app import app

    # Get all routes
    routes = [rule.rule for rule in app.url_map.iter_rules()]

    # Check auth routes
    assert "/auth/login" in routes, "Login route should exist"
    assert "/auth/logout" in routes, "Logout route should exist"
    assert "/auth/register" in routes, "Register route should exist"
    assert "/auth/profile" in routes, "Profile route should exist"


def test_templates_exist():
    """Test that auth templates exist"""
    import os

    templates_dir = "templates"
    assert os.path.exists(templates_dir), "Templates directory should exist"

    # Check required templates
    assert os.path.exists(
        os.path.join(templates_dir, "login.html")
    ), "login.html should exist"
    assert os.path.exists(
        os.path.join(templates_dir, "register.html")
    ), "register.html should exist"
    assert os.path.exists(
        os.path.join(templates_dir, "profile.html")
    ), "profile.html should exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
