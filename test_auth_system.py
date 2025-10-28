#!/usr/bin/env python3
"""
Test authentication system
"""
import sys
import auth_db

def test_user_authentication():
    """Test the authentication system"""
    print("=" * 60)
    print("Testing Authentication System")
    print("=" * 60)
    
    # Test 1: Get admin user
    print("\n1. Testing admin user retrieval...")
    admin = auth_db.get_user_by_username('admin')
    if admin:
        print("   ✓ Admin user found")
        print(f"     - Username: {admin['username']}")
        print(f"     - Email: {admin['email']}")
        print(f"     - Role: {admin['role']}")
    else:
        print("   ✗ Admin user not found")
        return False
    
    # Test 2: Verify correct password
    print("\n2. Testing password verification...")
    if auth_db.verify_password(admin, 'Admin@2025'):
        print("   ✓ Correct password verified successfully")
    else:
        print("   ✗ Password verification failed")
        return False
    
    # Test 3: Verify incorrect password
    print("\n3. Testing incorrect password...")
    if not auth_db.verify_password(admin, 'WrongPassword'):
        print("   ✓ Incorrect password rejected successfully")
    else:
        print("   ✗ Incorrect password was accepted (security issue!)")
        return False
    
    # Test 4: Test login attempts tracking
    print("\n4. Testing login attempt tracking...")
    auth_db.log_login_attempt('admin', '127.0.0.1', True)
    print("   ✓ Login attempt logged successfully")
    
    # Test 5: Check login attempts
    print("\n5. Testing login attempt checking...")
    can_login = auth_db.check_login_attempts('admin', '127.0.0.1')
    if can_login:
        print("   ✓ Login attempt check passed")
    else:
        print("   ✗ Login attempt check failed")
        return False
    
    # Test 6: Create test user
    print("\n6. Testing user creation...")
    result = auth_db.create_user(
        username='testuser',
        email='test@example.com',
        password='Test@123',
        role='user',
        name='Test User'
    )
    if result['success']:
        print("   ✓ Test user created successfully")
    else:
        print(f"   ✗ Failed to create user: {result.get('error', 'Unknown error')}")
        # This might fail if user already exists, which is okay
        if 'UNIQUE constraint failed' in result.get('error', ''):
            print("   (User already exists - continuing)")
        else:
            return False
    
    # Test 7: Get all users
    print("\n7. Testing get all users...")
    users = auth_db.get_all_users()
    if len(users) >= 1:  # At least admin should exist
        print(f"   ✓ Found {len(users)} users in database")
        for user in users:
            status = "Active" if user.get('is_active') else "Inactive"
            print(f"     - {user['username']} ({user['role']}) - {status}")
    else:
        print("   ✗ No users found")
        return False
    
    # Test 8: Test user exists check
    print("\n8. Testing user existence check...")
    if auth_db.user_exists(username='admin'):
        print("   ✓ Correctly identified existing user")
    else:
        print("   ✗ Failed to identify existing user")
        return False
    
    if not auth_db.user_exists(username='nonexistentuser'):
        print("   ✓ Correctly identified non-existent user")
    else:
        print("   ✗ False positive for non-existent user")
        return False
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    return True

if __name__ == '__main__':
    try:
        success = test_user_authentication()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
