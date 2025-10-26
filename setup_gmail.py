#!/usr/bin/env python3
"""
Gmail Setup Helper
Helps you set up Gmail App Password and test connection
"""

import smtplib
import json
import os
import time

def print_gmail_setup_instructions():
    """Print detailed Gmail setup instructions."""
    print("📧 Gmail Setup Instructions")
    print("=" * 60)
    print()
    print("🔐 Step 1: Enable 2-Factor Authentication")
    print("   1. Go to https://myaccount.google.com/security")
    print("   2. Click '2-Step Verification'")
    print("   3. Follow the setup process")
    print("   4. Make sure it's ENABLED")
    print()
    print("🔑 Step 2: Generate App Password")
    print("   1. Go to https://myaccount.google.com/security")
    print("   2. Click 'App passwords' (only visible with 2FA enabled)")
    print("   3. Select 'Mail' as the app")
    print("   4. Select 'Other' as the device")
    print("   5. Type 'Email Automation' as the name")
    print("   6. Click 'Generate'")
    print("   7. Copy the 16-character password (like: abcd efgh ijkl mnop)")
    print("   8. Remove spaces: abcdefghijklmnop")
    print()
    print("⏰ Step 3: Wait for Activation")
    print("   - New App Passwords can take 5-10 minutes to activate")
    print("   - Wait a few minutes before testing")
    print()
    print("🧪 Step 4: Test Connection")
    print("   - Run this script again to test")
    print("   - Or use: python test_connection.py")
    print()

def test_connection_with_retry(email, password, max_retries=3):
    """Test connection with retry logic."""
    print(f"🔍 Testing connection for {email}")
    print(f"🔑 Password: {'*' * len(password)} (length: {len(password)})")
    print()
    
    for attempt in range(max_retries):
        print(f"🔄 Attempt {attempt + 1}/{max_retries}")
        
        try:
            # Create SMTP connection
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
            server.starttls()
            server.login(email, password)
            server.quit()
            
            print("✅ Connection successful!")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
            if attempt < max_retries - 1:
                print("⏳ Waiting 30 seconds before retry...")
                time.sleep(30)
            else:
                print("\n🔧 Authentication failed after all retries.")
                print("Please check your App Password and try again.")
                return False
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
            if attempt < max_retries - 1:
                print("⏳ Waiting 10 seconds before retry...")
                time.sleep(10)
            else:
                print("\n🔧 Connection failed after all retries.")
                return False
    
    return False

def update_config_with_new_password():
    """Update config with new password from user input."""
    print("🔑 Enter New App Password")
    print("=" * 30)
    
    # Load current config
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "email": "othmanechaikhi.pro@gmail.com",
            "password": "",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "min_delay": 30,
            "max_delay": 60,
            "max_emails_per_day": 50
        }
    
    # Get new password from user
    print(f"Current email: {config['email']}")
    new_password = input("Enter new 16-character App Password: ").strip()
    
    if len(new_password) != 16:
        print("❌ App Password must be exactly 16 characters")
        return False
    
    # Update config
    config['password'] = new_password
    
    # Save config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Config updated with new password")
    return True

def main():
    """Main function."""
    print("🚀 Gmail Setup Helper")
    print("=" * 60)
    print()
    
    # Check if config exists
    config_file = "config.json"
    if not os.path.exists(config_file):
        print("❌ config.json not found")
        print("Please run the app first: python run_simple.py")
        return
    
    # Load config
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    email = config.get('email', '')
    password = config.get('password', '')
    
    if not email:
        print("❌ No email found in config")
        return
    
    print(f"📧 Email: {email}")
    print(f"🔑 Current password length: {len(password)}")
    print()
    
    # Show setup instructions
    print_gmail_setup_instructions()
    
    # Ask if user wants to update password
    if len(password) != 16:
        print("⚠️ Current password is not 16 characters")
        update_choice = input("Do you want to enter a new App Password? (y/n): ").lower()
        if update_choice == 'y':
            if update_config_with_new_password():
                # Reload config
                with open(config_file, 'r') as f:
                    config = json.load(f)
                password = config['password']
            else:
                return
        else:
            print("Please update your password manually in config.json")
            return
    
    # Test connection
    if password:
        print("\n🧪 Testing Connection")
        print("=" * 30)
        success = test_connection_with_retry(email, password)
        
        if success:
            print("\n🎉 Setup Complete!")
            print("Your Gmail is configured and ready to use.")
            print("\n🚀 To run the app:")
            print("   python run_simple.py")
        else:
            print("\n⚠️ Setup incomplete. Please follow the instructions above.")
    else:
        print("❌ No password configured")
        print("Please update config.json with your App Password")

if __name__ == "__main__":
    main()
