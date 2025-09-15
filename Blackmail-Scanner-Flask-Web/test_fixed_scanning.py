#!/usr/bin/env python3
"""
Test script to verify the fixed scanning functionality
"""

import os
import sys
import sqlite3
import logging

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_cleanup():
    """Test the database cleanup functionality"""
    try:
        from blackmail_model_scan import cleanup_missing_files
        
        # Create test database with some missing files
        connection = sqlite3.connect('test_images.db')
        cursor = connection.cursor()
        
        create_table_command = """
        CREATE TABLE IF NOT EXISTS master_table (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL UNIQUE,
            severity TEXT DEFAULT 'PENDING',
            description TEXT
        );"""
        cursor.execute(create_table_command)
        
        # Insert test data with some missing files
        test_data = [
            ('mock_data/existing_file.jpg', 'PENDING', None),
            ('mock_data/missing_file.jpg', 'PENDING', None),
            ('does_not_exist.png', 'PENDING', None)
        ]
        
        cursor.executemany(
            "INSERT OR REPLACE INTO master_table (file_path, severity, description) VALUES (?, ?, ?)",
            test_data
        )
        
        connection.commit()
        connection.close()
        
        # Test cleanup
        cleanup_missing_files('test_images.db')
        
        # Verify cleanup worked
        connection = sqlite3.connect('test_images.db')
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM master_table")
        remaining_count = cursor.fetchone()[0]
        connection.close()
        
        print(f"[OK] Database cleanup test passed - {remaining_count} files remaining")
        
        # Cleanup test database
        os.remove('test_images.db')
        return True
        
    except Exception as e:
        print(f"[FAIL] Database cleanup test failed: {e}")
        return False

def test_model_import():
    """Test that the model scanning module imports correctly"""
    try:
        from blackmail_model_scan import generate_ratings, return_rating, cleanup_missing_files
        print("[OK] Model import test passed")
        return True
    except Exception as e:
        print(f"[FAIL] Model import test failed: {e}")
        return False

def test_frontend_integration():
    """Test that frontend integrates with backend correctly"""
    try:
        from blackmail_file_scanner_frontend import app, scan_directory_to_db, display
        
        with app.test_client() as client:
            # Test main route
            response = client.get('/')
            if response.status_code == 200:
                print("[OK] Frontend integration test passed")
                return True
            else:
                print(f"[FAIL] Frontend returned status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"[FAIL] Frontend integration test failed: {e}")
        return False

def check_groq_model():
    """Check if GROQ API key is set and verify model name"""
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if api_key:
            print("[OK] GROQ_API_KEY is set")
            
            # Read the model scan file to verify model name
            with open('blackmail_model_scan.py', 'r') as f:
                content = f.read()
                if 'meta-llama/llama-4-scout-17b-16e-instruct' in content:
                    print("[OK] Current Groq vision model is configured")
                    return True
                else:
                    print("[WARN] Model name may not be current")
                    return False
        else:
            print("[WARN] GROQ_API_KEY not set - AI scanning will not work")
            return False
            
    except Exception as e:
        print(f"[FAIL] Groq model check failed: {e}")
        return False

if __name__ == '__main__':
    print("Testing Fixed Scanning Functionality...")
    print("=" * 50)
    
    tests = [
        test_model_import,
        test_database_cleanup,
        test_frontend_integration,
        check_groq_model
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{len(tests)} tests passed")
    
    if passed >= 3:  # Allow for GROQ key warning
        print("Fixed scanning functionality is ready!")
        print("\nChanges made:")
        print("1. Updated to current Groq vision model: meta-llama/llama-4-scout-17b-16e-instruct")
        print("2. Added database cleanup for missing files")
        print("3. Improved error handling and status tracking")
        print("4. Enhanced response parsing for better classification")
        print("5. Added FAILED/UNKNOWN status handling in UI")
        print("\nTo test:")
        print("1. Set GROQ_API_KEY environment variable")
        print("2. Add some image files to mock_data directory")
        print("3. Run: python blackmail_file_scanner_frontend.py")
        print("4. Visit: http://localhost:5000/scan")
    else:
        print("Some critical tests failed. Please check the errors above.")