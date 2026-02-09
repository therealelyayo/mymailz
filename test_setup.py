#!/usr/bin/env python3
"""
Test script to verify the MyMailz application structure and imports.
This script checks that all components are properly configured.
"""

import os
import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        from flask import Flask, render_template, request, jsonify
        print("✓ Flask imports successful")
        
        from dotenv import load_dotenv
        print("✓ python-dotenv import successful")
        
        from nylas import Client
        print("✓ Nylas SDK import successful")
        
        from datetime import datetime
        print("✓ datetime import successful")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md',
        'templates/index.html'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_environment_config():
    """Test environment configuration"""
    print("\nTesting environment configuration...")
    
    if os.path.exists('.env.example'):
        with open('.env.example', 'r') as f:
            content = f.read()
            required_vars = ['NYLAS_API_KEY', 'NYLAS_API_URI', 'NYLAS_GRANT_ID']
            all_present = all(var in content for var in required_vars)
            
            if all_present:
                print("✓ All required environment variables defined in .env.example")
                return True
            else:
                print("✗ Some environment variables missing from .env.example")
                return False
    else:
        print("✗ .env.example file not found")
        return False

def test_flask_app():
    """Test that Flask app can be initialized"""
    print("\nTesting Flask application...")
    try:
        # Set dummy environment variables
        os.environ['NYLAS_API_KEY'] = 'test_key'
        os.environ['NYLAS_API_URI'] = 'https://api.us.nylas.com'
        os.environ['NYLAS_GRANT_ID'] = 'test_grant_id'
        
        from app import app
        
        if app:
            print("✓ Flask app initialized successfully")
            print(f"✓ App name: {app.name}")
            
            # Check routes
            routes = [str(rule) for rule in app.url_map.iter_rules()]
            expected_routes = ['/', '/api/grant-id', '/api/emails', '/api/email/<email_id>']
            
            print(f"✓ Registered routes: {len(routes)}")
            for route in expected_routes:
                if any(route in r for r in routes):
                    print(f"  ✓ {route}")
                else:
                    print(f"  ✗ {route} not found")
            
            return True
        else:
            print("✗ Failed to initialize Flask app")
            return False
    except Exception as e:
        print(f"✗ Error initializing Flask app: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("MyMailz Application Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_file_structure,
        test_environment_config,
        test_flask_app
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Application is ready to use.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your Nylas API credentials to .env")
        print("3. Run: python app.py")
        print("4. Open http://localhost:5000 in your browser")
        return 0
    else:
        print("✗ Some tests failed. Please check the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
