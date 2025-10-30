#!/usr/bin/env python3
"""
سكريبت التحقق من جاهزية النشر
Deployment Readiness Verification Script
نظام إدارة الإسكان الجامعي
"""

import os
import sys
import sqlite3
from pathlib import Path

# Colors for output
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color


def print_header(text):
    """Print section header"""
    print(f"\n{BLUE}{'='*60}{NC}")
    print(f"{BLUE}{text}{NC}")
    print(f"{BLUE}{'='*60}{NC}\n")


def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓{NC} {text}")


def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠{NC} {text}")


def print_error(text):
    """Print error message"""
    print(f"{RED}✗{NC} {text}")


def check_files():
    """Check existence of critical files"""
    print_header("1. فحص الملفات الأساسية / Checking Critical Files")
    
    required_files = {
        'app.py': 'التطبيق الرئيسي / Main application',
        'database_api.py': 'واجهة قاعدة البيانات / Database API',
        'requirements.txt': 'المكتبات المطلوبة / Requirements',
        'housing_database.db': 'قاعدة البيانات / Database',
        'Procfile': 'ملف النشر / Deployment file',
        'render.yaml': 'إعدادات Render / Render config',
        'runtime.txt': 'إصدار Python / Python version'
    }
    
    all_good = True
    for file, desc in required_files.items():
        if os.path.exists(file):
            print_success(f"{file} - {desc}")
        else:
            print_error(f"{file} - {desc} - مفقود / Missing")
            all_good = False
    
    return all_good


def check_database():
    """Check database integrity and data"""
    print_header("2. فحص قاعدة البيانات / Checking Database")
    
    if not os.path.exists('housing_database.db'):
        print_error("قاعدة البيانات مفقودة / Database missing")
        return False
    
    try:
        conn = sqlite3.connect('housing_database.db')
        cursor = conn.cursor()
        
        # Check tables
        tables = {
            'residents': 'السكان / Residents',
            'buildings': 'المباني / Buildings',
            'units': 'الوحدات السكنية / Units',
            'vehicle_stickers': 'ملصقات السيارات / Vehicle Stickers',
            'parking_spots': 'المواقف / Parking Spots'
        }
        
        for table, desc in tables.items():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            if count > 0:
                print_success(f"{table}: {count} {desc}")
            else:
                print_warning(f"{table}: 0 {desc} - فارغ / Empty")
        
        conn.close()
        return True
    except Exception as e:
        print_error(f"خطأ في قاعدة البيانات / Database error: {e}")
        return False


def check_static_files():
    """Check static files and directories"""
    print_header("3. فحص الملفات الثابتة / Checking Static Files")
    
    if not os.path.exists('static'):
        print_error("مجلد static مفقود / Static folder missing")
        return False
    
    # Count HTML files
    html_files = list(Path('static').glob('*.html'))
    print_success(f"عدد ملفات HTML / HTML files: {len(html_files)}")
    
    # Check important HTML files
    important_pages = [
        'index.html',
        'main_portal.html',
        'interactive_dashboard.html',
        'login.html'
    ]
    
    for page in important_pages:
        path = f'static/{page}'
        if os.path.exists(path):
            print_success(f"{page} - موجود / Present")
        else:
            print_warning(f"{page} - مفقود / Missing")
    
    return True


def check_dependencies():
    """Check Python dependencies"""
    print_header("4. فحص المكتبات / Checking Dependencies")
    
    # Map package names to their import names
    required_packages = {
        'Flask': 'flask',
        'gunicorn': 'gunicorn',
        'Pillow': 'PIL',
        'openai': 'openai',
        'Flask-Login': 'flask_login',
        'bcrypt': 'bcrypt'
    }
    
    all_installed = True
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
            print_success(f"{package} - مثبت / Installed")
        except ImportError:
            print_error(f"{package} - غير مثبت / Not installed")
            all_installed = False
    
    return all_installed


def check_directories():
    """Check and create necessary directories"""
    print_header("5. فحص المجلدات / Checking Directories")
    
    required_dirs = ['uploads', 'processed_images', 'logs']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print_success(f"{dir_name} - موجود / Exists")
        else:
            print_warning(f"{dir_name} - غير موجود، سيتم إنشاؤه / Missing, will be created")
            try:
                os.makedirs(dir_name, exist_ok=True)
                print_success(f"{dir_name} - تم الإنشاء / Created")
            except Exception as e:
                print_error(f"{dir_name} - فشل الإنشاء / Creation failed: {e}")
    
    return True


def check_environment():
    """Check environment variables and configuration"""
    print_header("6. فحص متغيرات البيئة / Checking Environment Variables")
    
    env_vars = {
        'OPENAI_API_KEY': 'مفتاح OpenAI / OpenAI API Key',
        'SECRET_KEY': 'مفتاح Flask السري / Flask Secret Key',
        'FLASK_ENV': 'بيئة Flask / Flask Environment'
    }
    
    for var, desc in env_vars.items():
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var:
                masked = value[:8] + '...' if len(value) > 8 else '***'
                print_success(f"{var} = {masked} - {desc}")
            else:
                print_success(f"{var} = {value} - {desc}")
        else:
            if var == 'OPENAI_API_KEY':
                print_warning(f"{var} - غير معيّن / Not set - {desc} (ضروري للتعرف على اللوحات / Required for plate recognition)")
            else:
                print_warning(f"{var} - غير معيّن / Not set - {desc} (سيتم التوليد تلقائياً / Will be auto-generated)")
    
    return True


def check_app_configuration():
    """Check Flask app configuration"""
    print_header("7. فحص إعدادات التطبيق / Checking App Configuration")
    
    try:
        # Import app to check configuration
        import app as application
        import database_api
        
        checks = {
            'Flask app exists': hasattr(application, 'app'),
            'Secret key configured': bool(application.app.secret_key) if hasattr(application, 'app') else False,
            'Static folder configured': os.path.exists('static'),
            'Database API available': True  # Already imported above
        }
        
        for check, passed in checks.items():
            if passed:
                print_success(check)
            else:
                print_error(check)
        
        return all(checks.values())
    except Exception as e:
        print_error(f"خطأ في التحقق من التطبيق / App verification error: {e}")
        return False


def generate_summary(results):
    """Generate deployment readiness summary"""
    print_header("ملخص التحقق / Verification Summary")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    print(f"إجمالي الفحوصات / Total Checks: {total}")
    print_success(f"نجحت / Passed: {passed}")
    
    if failed > 0:
        print_error(f"فشلت / Failed: {failed}")
    
    print()
    
    if passed == total:
        print_success("✅ النظام جاهز تماماً للنشر! / System fully ready for deployment!")
        print()
        print(f"{GREEN}يمكنك الآن نشر النظام على المنصة المفضلة:{NC}")
        print("  • Railway.app (موصى به / Recommended)")
        print("  • Render.com")
        print("  • PythonAnywhere")
        print("  • Vercel")
        print()
        print(f"{YELLOW}لا تنس تعيين متغير البيئة:{NC}")
        print("  OPENAI_API_KEY=your-api-key-here")
    else:
        print_warning("⚠️  يوجد بعض المشاكل التي يجب حلها قبل النشر / Some issues need to be resolved before deployment")
        print()
        print("الفحوصات الفاشلة / Failed Checks:")
        for check, result in results.items():
            if not result:
                print(f"  • {check}")
    
    print()
    return passed == total


def main():
    """Main verification function"""
    print_header("🔍 التحقق من جاهزية النشر / Deployment Readiness Verification")
    print("نظام إدارة الإسكان الجامعي / Faculty Housing Management System")
    print("جامعة الإمام محمد بن سعود الإسلامية")
    print()
    
    results = {
        'Files Check': check_files(),
        'Database Check': check_database(),
        'Static Files Check': check_static_files(),
        'Dependencies Check': check_dependencies(),
        'Directories Check': check_directories(),
        'Environment Check': check_environment(),
        'App Configuration Check': check_app_configuration()
    }
    
    success = generate_summary(results)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
