#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XAMPP Setup Test Script
سكريبت اختبار إعداد XAMPP

This script tests the environment setup for running the Housing Management System on XAMPP.
يختبر هذا السكريبت إعداد البيئة لتشغيل نظام إدارة الإسكان على XAMPP.

Usage / الاستخدام:
    python test_xampp_setup.py
"""

import sys
import os
import platform
from pathlib import Path

# Color codes for terminal output
# رموز الألوان لإخراج Terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    INFO = '\033[96m'  # Cyan for info messages
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header / طباعة عنوان منسق"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """Print success message / طباعة رسالة نجاح"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Print error message / طباعة رسالة خطأ"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    """Print warning message / طباعة رسالة تحذير"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    """Print info message / طباعة رسالة معلومات"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def test_python_version():
    """Test Python version / اختبار إصدار Python"""
    print_header("Testing Python Version / اختبار إصدار Python")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"Python version: {version_str}")
    print_info(f"Python executable: {sys.executable}")
    
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version_str} is compatible (3.11+ required)")
        return True
    elif version.major == 3 and version.minor >= 8:
        print_warning(f"Python {version_str} might work but 3.11+ is recommended")
        return True
    else:
        print_error(f"Python {version_str} is too old. Python 3.11+ required")
        return False

def test_required_modules():
    """Test if required Python modules are installed / اختبار المكتبات المطلوبة"""
    print_header("Testing Required Modules / اختبار المكتبات المطلوبة")
    
    required_modules = [
        ('flask', 'Flask'),
        ('werkzeug', 'Werkzeug'),
        ('PIL', 'Pillow'),
        ('dotenv', 'python-dotenv'),
    ]
    
    all_found = True
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print_success(f"{package_name} is installed")
        except ImportError:
            print_error(f"{package_name} is NOT installed")
            print_info(f"  Install with: pip install {package_name}")
            all_found = False
    
    # Test optional modules
    print_info("\nOptional modules:")
    optional_modules = [
        ('openai', 'openai'),
        ('easyocr', 'easyocr'),
        ('cv2', 'opencv-python'),
    ]
    
    for module_name, package_name in optional_modules:
        try:
            __import__(module_name)
            print_success(f"{package_name} is installed")
        except ImportError:
            print_warning(f"{package_name} is NOT installed (optional)")
    
    return all_found

def test_project_files():
    """Test if required project files exist / اختبار وجود ملفات المشروع"""
    print_header("Testing Project Files / اختبار ملفات المشروع")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'housing_database.db',
        'database_api.py',
        'config.py',
    ]
    
    all_found = True
    for filename in required_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print_success(f"{filename} exists ({size:,} bytes)")
        else:
            print_error(f"{filename} NOT FOUND")
            all_found = False
    
    # Test directories
    print_info("\nChecking directories:")
    required_dirs = ['static', 'uploads', 'processed_images', 'logs']
    for dirname in required_dirs:
        if os.path.exists(dirname):
            print_success(f"{dirname}/ exists")
        else:
            print_warning(f"{dirname}/ does not exist (will be created automatically)")
    
    return all_found

def test_env_file():
    """Test .env file / اختبار ملف .env"""
    print_header("Testing Environment File / اختبار ملف البيئة")
    
    if os.path.exists('.env'):
        print_success(".env file exists")
        
        # Try to load and check for required variables
        with open('.env', 'r') as f:
            content = f.read()
            
        required_vars = ['OPENAI_API_KEY', 'SECRET_KEY', 'DATABASE_PATH']
        for var in required_vars:
            if var in content:
                print_success(f"{var} is defined in .env")
            else:
                print_warning(f"{var} is NOT defined in .env")
        
        return True
    else:
        print_error(".env file NOT FOUND")
        print_info("Create .env file with the following content:")
        print_info("  OPENAI_API_KEY=your-api-key-here")
        print_info("  FLASK_ENV=production")
        print_info("  SECRET_KEY=your-secret-key")
        print_info("  DATABASE_PATH=housing_database.db")
        return False

def test_app_import():
    """Test if the app can be imported / اختبار استيراد التطبيق"""
    print_header("Testing App Import / اختبار استيراد التطبيق")
    
    try:
        from app import app
        print_success("app.py imports successfully")
        print_info(f"Flask app name: {app.name}")
        return True
    except Exception as e:
        print_error(f"Failed to import app: {str(e)}")
        return False

def test_database_connection():
    """Test database connection / اختبار الاتصال بقاعدة البيانات"""
    print_header("Testing Database / اختبار قاعدة البيانات")
    
    try:
        import sqlite3
        conn = sqlite3.connect('housing_database.db')
        cursor = conn.cursor()
        
        # Test some tables
        tables = ['residents', 'buildings', 'units', 'vehicle_stickers']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print_success(f"Table '{table}' exists with {count} records")
        
        conn.close()
        return True
    except Exception as e:
        print_error(f"Database error: {str(e)}")
        return False

def test_port_availability():
    """Test if the default port is available / اختبار توفر المنفذ الافتراضي"""
    print_header("Testing Port Availability / اختبار توفر المنفذ")
    
    import socket
    port = 5000
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    
    if result == 0:
        print_warning(f"Port {port} is already in use")
        print_info("  You may need to stop the running service or use a different port")
        return False
    else:
        print_success(f"Port {port} is available")
        return True

def print_system_info():
    """Print system information / طباعة معلومات النظام"""
    print_header("System Information / معلومات النظام")
    
    print_info(f"Operating System: {platform.system()} {platform.release()}")
    print_info(f"Platform: {platform.platform()}")
    print_info(f"Machine: {platform.machine()}")
    print_info(f"Processor: {platform.processor()}")
    print_info(f"Python Implementation: {platform.python_implementation()}")
    print_info(f"Current Directory: {os.getcwd()}")

def main():
    """Main test function / الدالة الرئيسية للاختبار"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("=" * 60)
    print("XAMPP Setup Test Script".center(60))
    print("سكريبت اختبار إعداد XAMPP".center(60))
    print("=" * 60)
    print(f"{Colors.RESET}\n")
    
    # Run all tests
    results = []
    
    print_system_info()
    
    results.append(('Python Version', test_python_version()))
    results.append(('Required Modules', test_required_modules()))
    results.append(('Project Files', test_project_files()))
    results.append(('Environment File', test_env_file()))
    results.append(('App Import', test_app_import()))
    results.append(('Database', test_database_connection()))
    results.append(('Port Availability', test_port_availability()))
    
    # Print summary
    print_header("Test Summary / ملخص الاختبارات")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{Colors.BOLD}Tests Passed: {passed}/{total}{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed! Your XAMPP setup is ready!{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}✓ جميع الاختبارات نجحت! إعداد XAMPP جاهز!{Colors.RESET}")
        print(f"\n{Colors.INFO}You can now start the application with:{Colors.RESET}")
        if platform.system() == 'Windows':
            print(f"  {Colors.BLUE}start_flask_windows.bat{Colors.RESET}")
        else:
            print(f"  {Colors.BLUE}./start_flask_linux.sh{Colors.RESET}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed. Please fix the issues above.{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BOLD}✗ بعض الاختبارات فشلت. يرجى إصلاح المشاكل أعلاه.{Colors.RESET}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
