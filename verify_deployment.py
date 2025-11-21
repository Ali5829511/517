#!/usr/bin/env python3
"""
Deployment Verification Script
سكريبت التحقق من النشر

This script verifies that the application is deployed correctly
and all endpoints are working.

Usage:
    python verify_deployment.py https://your-app.railway.app
"""

import sys
import requests
import json
from datetime import datetime


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def print_success(text):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"❌ {text}")


def print_warning(text):
    """Print warning message"""
    print(f"⚠️  {text}")


def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")


def verify_endpoint(base_url, endpoint, description):
    """Verify a single endpoint"""
    url = f"{base_url}{endpoint}"
    print(f"\nChecking: {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print_success(f"Status: {response.status_code} OK")
            
            # Try to parse JSON if it's a JSON endpoint
            if endpoint.startswith('/api/'):
                try:
                    data = response.json()
                    print_info(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
                    return True, data
                except (json.JSONDecodeError, ValueError) as e:
                    print_info(f"Response is not valid JSON: {e}")
                    return True, None
            else:
                print_info(f"Content length: {len(response.content)} bytes")
                return True, None
        else:
            print_error(f"Status: {response.status_code}")
            return False, None
            
    except requests.exceptions.Timeout:
        print_error("Request timed out")
        return False, None
    except requests.exceptions.ConnectionError:
        print_error("Connection failed")
        return False, None
    except requests.exceptions.RequestException as e:
        print_error(f"Request error: {str(e)}")
        return False, None
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False, None


def main():
    """Main verification function"""
    if len(sys.argv) < 2:
        print("Usage: python verify_deployment.py <base_url>")
        print("Example: python verify_deployment.py https://your-app.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print_header("نظام إدارة الإسكان الجامعي - Deployment Verification")
    print(f"Verifying deployment at: {base_url}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # List of endpoints to check
    endpoints = [
        ("/", "Main Page"),
        ("/api/version", "Version Information"),
        ("/api/statistics", "System Statistics"),
        ("/static/main_portal.html", "Main Portal"),
        ("/static/comprehensive_system_report.html", "Comprehensive Report"),
    ]
    
    results = []
    version_data = None
    
    for endpoint, description in endpoints:
        success, data = verify_endpoint(base_url, endpoint, description)
        results.append((endpoint, success))
        
        if endpoint == "/api/version" and data:
            version_data = data
    
    # Print summary
    print_header("Verification Summary - ملخص التحقق")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    # Show version information if available
    if version_data:
        print_header("Deployment Information - معلومات النشر")
        data = version_data.get('data', {})
        print(f"App Name: {data.get('app_name', 'N/A')}")
        print(f"Version: {data.get('version', 'N/A')}")
        print(f"Deployment Date: {data.get('deployment_date', 'N/A')}")
        print(f"Git Commit: {data.get('git_commit', 'N/A')}")
        print(f"Status: {data.get('status', 'N/A')}")
        
        if 'database' in data:
            db = data['database']
            if isinstance(db, dict):
                print("\nDatabase Statistics:")
                print(f"  Residents: {db.get('residents', 'N/A')}")
                print(f"  Buildings: {db.get('buildings', 'N/A')}")
                print(f"  Units: {db.get('units', 'N/A')}")
                print(f"  Stickers: {db.get('stickers', 'N/A')}")
                print(f"  Parking: {db.get('parking_spots', 'N/A')}")
    
    # Final result
    print_header("Final Result - النتيجة النهائية")
    
    if passed == total:
        print_success("All checks passed! Deployment is successful.")
        print_success("جميع الفحوصات نجحت! النشر ناجح.")
        return 0
    else:
        print_error(f"{total - passed} check(s) failed. Please review the errors above.")
        print_error(f"فشل {total - passed} فحص. يرجى مراجعة الأخطاء أعلاه.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
