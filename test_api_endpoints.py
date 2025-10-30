#!/usr/bin/env python3
"""
اختبار نقاط النهاية API
API Endpoints Test
نظام إدارة الإسكان الجامعي
"""

import sys
import json
from app import app

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


def print_error(text):
    """Print error message"""
    print(f"{RED}✗{NC} {text}")


def test_endpoint(client, endpoint, description):
    """Test a single API endpoint"""
    try:
        response = client.get(endpoint)
        
        if response.status_code == 200:
            # Try to parse JSON
            try:
                data = json.loads(response.data)
                if isinstance(data, list):
                    count = len(data)
                    print_success(f"{endpoint} - {description} - {count} عنصر / items")
                elif isinstance(data, dict):
                    count = len(data)
                    print_success(f"{endpoint} - {description} - {count} مفتاح / keys")
                else:
                    print_success(f"{endpoint} - {description} - يعمل / Working")
                return True
            except:
                print_success(f"{endpoint} - {description} - يعمل / Working")
                return True
        else:
            print_error(f"{endpoint} - {description} - رمز الحالة / Status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"{endpoint} - {description} - خطأ / Error: {e}")
        return False


def main():
    """Main test function"""
    print_header("🔍 اختبار نقاط النهاية API / Testing API Endpoints")
    print("نظام إدارة الإسكان الجامعي / Faculty Housing Management System")
    print()
    
    # Create test client
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Define API endpoints to test
    endpoints = [
        ('/api/residents', 'بيانات السكان / Residents data'),
        ('/api/buildings', 'بيانات المباني / Buildings data'),
        ('/api/stickers', 'بيانات الملصقات / Stickers data'),
        ('/api/parking', 'بيانات المواقف / Parking data'),
        ('/api/statistics', 'الإحصائيات / Statistics'),
        ('/api/processed-images-stats', 'إحصائيات الصور المعالجة / Processed images stats'),
    ]
    
    results = []
    for endpoint, description in endpoints:
        result = test_endpoint(client, endpoint, description)
        results.append(result)
    
    print()
    print_header("النتيجة / Summary")
    
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"إجمالي الاختبارات / Total Tests: {total}")
    print_success(f"نجحت / Passed: {passed}")
    
    if failed > 0:
        print_error(f"فشلت / Failed: {failed}")
    else:
        print()
        print_success("✅ جميع نقاط النهاية API تعمل بشكل صحيح!")
        print_success("✅ All API endpoints working correctly!")
    
    print()
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
