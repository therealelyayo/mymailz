#!/usr/bin/env python3
"""
Test script for connection testing and folder listing functionality.
"""

import os
import sys
import json

# Set up test environment before importing app
os.environ['NYLAS_API_KEY'] = 'test_key'
os.environ['NYLAS_API_URI'] = 'https://api.us.nylas.com'
os.environ['NYLAS_GRANT_ID'] = 'test_grant_id'

def test_api_routes_exist():
    """Test that the new API routes are registered"""
    print("Testing API routes...")
    try:
        from app import app
        
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        # Check for folders endpoint
        assert any('/api/folders' in route for route in routes), "Folders endpoint should exist"
        print("✓ /api/folders endpoint exists")
        
        # Check for grant-id endpoint (should already exist)
        assert any('/api/grant-id' in route for route in routes), "Grant ID endpoint should exist"
        print("✓ /api/grant-id endpoint exists")
        
        return True
    except Exception as e:
        print(f"✗ API routes test error: {e}")
        return False

def test_connection_function_exists():
    """Test that the connection test function exists"""
    print("\nTesting connection test function...")
    try:
        from app import test_connection_status
        
        assert callable(test_connection_status), "test_connection_status should be callable"
        print("✓ test_connection_status function exists")
        
        return True
    except Exception as e:
        print(f"✗ Connection function test error: {e}")
        return False

def test_folders_endpoint_requires_grant_id():
    """Test the folders endpoint requires grant ID"""
    print("\nTesting folders endpoint requires grant ID...")
    try:
        from app import app
        
        # Create test client
        client = app.test_client()
        
        # Test without grant ID
        app.config['CURRENT_GRANT_ID'] = ''
        response = client.get('/api/folders')
        assert response.status_code == 400, "Should return 400 without grant ID"
        data = json.loads(response.data)
        assert data['success'] == False, "Should indicate failure"
        assert 'Grant ID not set' in data['message'], "Should mention grant ID not set"
        print("✓ Folders endpoint returns error without grant ID")
        
        return True
    except Exception as e:
        print(f"✗ Folders endpoint test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_grant_id_endpoint_structure():
    """Test grant ID endpoint has connection status in response structure"""
    print("\nTesting grant ID endpoint structure...")
    try:
        from app import app
        import inspect
        from app import manage_grant_id
        
        # Check the source code to see if connection is added
        source = inspect.getsource(manage_grant_id)
        assert 'connection' in source.lower(), "manage_grant_id should reference connection"
        assert 'test_connection_status' in source, "manage_grant_id should call test_connection_status"
        print("✓ Grant ID endpoint includes connection testing")
        
        return True
    except Exception as e:
        print(f"✗ Grant ID structure test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_html_has_folders_section():
    """Test that HTML template has folders section"""
    print("\nTesting HTML template...")
    try:
        with open('templates/index.html', 'r') as f:
            html = f.read()
        
        assert 'Folders' in html or 'folders' in html, "HTML should mention folders"
        assert 'loadFolders' in html, "HTML should have loadFolders function"
        assert '/api/folders' in html, "HTML should reference folders API"
        assert 'connectionStatus' in html or 'connection' in html.lower(), "HTML should have connection status"
        print("✓ HTML template includes folders section")
        print("✓ HTML template includes connection status display")
        print("✓ HTML template includes loadFolders function")
        
        return True
    except Exception as e:
        print(f"✗ HTML template test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Connection and Folders Test Suite")
    print("=" * 60)
    
    tests = [
        test_api_routes_exist,
        test_connection_function_exists,
        test_folders_endpoint_requires_grant_id,
        test_grant_id_endpoint_structure,
        test_html_has_folders_section
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
        print("✓ All tests passed!")
        print("\nImplementation complete:")
        print("1. ✓ Connection test added when grant ID is saved")
        print("2. ✓ Folders endpoint added to list mailbox folders")
        print("3. ✓ UI updated to show connection status")
        print("4. ✓ UI updated to display folders")
        return 0
    else:
        print("✗ Some tests failed. Please check the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
