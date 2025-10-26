#!/usr/bin/env python3
"""
Test the email automation app
"""

import json
import os

def test_config():
    """Test configuration loading."""
    print("🔍 Testing configuration...")
    
    try:
        if os.path.exists("config.json"):
            with open("config.json", 'r') as f:
                config = json.load(f)
            print(f"✅ Config loaded: {config.get('email', 'NO EMAIL')}")
            print(f"✅ Password length: {len(config.get('password', ''))}")
            return True
        else:
            print("❌ config.json not found")
            return False
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False

def test_recipients():
    """Test recipients loading."""
    print("🔍 Testing recipients...")
    
    try:
        if os.path.exists("recipients.json"):
            with open("recipients.json", 'r') as f:
                recipients = json.load(f)
            print(f"✅ Recipients loaded: {len(recipients)} recipients")
            for i, r in enumerate(recipients[:3]):  # Show first 3
                print(f"   {i+1}. {r.get('email', 'NO EMAIL')}")
            return True
        else:
            print("❌ recipients.json not found")
            return False
    except Exception as e:
        print(f"❌ Error loading recipients: {e}")
        return False

def test_imports():
    """Test importing required modules."""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import smtplib
        print("✅ smtplib imported")
    except ImportError as e:
        print(f"❌ smtplib import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ pandas imported")
    except ImportError as e:
        print(f"⚠️ pandas import failed: {e}")
        print("   (This might cause issues)")
    
    return True

def main():
    """Run all tests."""
    print("🧪 Testing Email Automation App")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Recipients", test_recipients)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 {name}:")
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! The app should work.")
        print("\n🚀 To run the app:")
        print("   python run_simple.py")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("\n🔧 To fix issues:")
        print("   1. Install missing dependencies: pip install streamlit pandas")
        print("   2. Check your configuration files")
        print("   3. Make sure all files are in the same directory")

if __name__ == "__main__":
    main()
