#!/usr/bin/env python3
"""
Test Gmail Connection and Help Generate App Password
"""

import smtplib
import json
import os

def test_gmail_connection(email, password):
    """Test Gmail connection with detailed error messages."""
    print("🔍 Testing Gmail Connection")
    print("=" * 50)
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {'*' * len(password)} (length: {len(password)})")
    print(f"📡 SMTP: smtp.gmail.com:587")
    print("-" * 50)
    
    try:
        # Create SMTP connection
        print("🔗 Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        
        print("🔒 Starting TLS encryption...")
        server.starttls()
        
        print("🔐 Attempting authentication...")
        server.login(email, password)
        
        print("✅ Authentication successful!")
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("❌ Authentication failed!")
        print(f"Error: {e}")
        print("\n🔧 Troubleshooting Steps:")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Click 'App passwords' (only visible with 2FA enabled)")
        print("3. Delete the old password and create a new one")
        print("4. Copy the NEW 16-character password")
        print("5. Make sure 2-Factor Authentication is enabled")
        print("6. Wait 5-10 minutes for the new password to activate")
        return False
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    """Main function."""
    print("📧 Gmail Connection Tester")
    print("=" * 50)
    
    # Load config
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        email = config.get('email', '')
        password = config.get('password', '')
        
        if not email or not password:
            print("❌ No email or password found in config.json")
            print("Please run the app first and configure your settings.")
            return
        
        # Test connection
        success = test_gmail_connection(email, password)
        
        if success:
            print("\n🎉 Connection successful! Your app should work.")
            print("\n🚀 To run the app:")
            print("   python run_simple.py")
        else:
            print("\n⚠️ Connection failed. Please follow the troubleshooting steps above.")
            print("\nAfter generating a new App Password:")
            print("1. Update config.json with the new password")
            print("2. Run this test again")
            print("3. Then run the app")
    else:
        print("❌ config.json not found")
        print("Please run the app first: python run_simple.py")

if __name__ == "__main__":
    main()
