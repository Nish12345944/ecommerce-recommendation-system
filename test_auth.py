#!/usr/bin/env python3
"""
Simple test script to verify authentication functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'E-Commerece-Recommendation-System-Machine-Learning-Product-Recommendation-system-'))

from werkzeug.security import generate_password_hash, check_password_hash

def test_password_hashing():
    """Test password hashing functionality"""
    print("Testing password hashing...")
    
    # Test password
    password = "testpassword123"
    
    # Hash the password
    hashed = generate_password_hash(password)
    print(f"Original password: {password}")
    print(f"Hashed password: {hashed}")
    
    # Verify the password
    is_valid = check_password_hash(hashed, password)
    print(f"Password verification: {'PASSED' if is_valid else 'FAILED'}")
    
    # Test with wrong password
    wrong_password = "wrongpassword"
    is_invalid = check_password_hash(hashed, wrong_password)
    print(f"Wrong password verification: {'FAILED (Good!)' if not is_invalid else 'PASSED (Bad!)'}")
    
    return is_valid and not is_invalid

def test_email_validation():
    """Test email validation regex"""
    import re
    
    print("\nTesting email validation...")
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    valid_emails = [
        "test@example.com",
        "user.name@domain.co.uk",
        "user+tag@example.org"
    ]
    
    invalid_emails = [
        "invalid-email",
        "@example.com",
        "test@",
        "test.example.com"
    ]
    
    all_passed = True
    
    for email in valid_emails:
        is_valid = bool(re.match(email_pattern, email))
        print(f"Valid email '{email}': {'PASSED' if is_valid else 'FAILED'}")
        if not is_valid:
            all_passed = False
    
    for email in invalid_emails:
        is_invalid = bool(re.match(email_pattern, email))
        print(f"Invalid email '{email}': {'PASSED' if not is_invalid else 'FAILED'}")
        if is_invalid:
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("=== Authentication System Tests ===\n")
    
    password_test = test_password_hashing()
    email_test = test_email_validation()
    
    print(f"\n=== Test Results ===")
    print(f"Password hashing: {'PASSED' if password_test else 'FAILED'}")
    print(f"Email validation: {'PASSED' if email_test else 'FAILED'}")
    print(f"Overall: {'ALL TESTS PASSED' if password_test and email_test else 'SOME TESTS FAILED'}")