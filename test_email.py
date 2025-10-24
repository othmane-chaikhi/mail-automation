#!/usr/bin/env python3
"""
Email Test Script
Test your email configuration before running the full automation.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_config():
    """Load configuration from config.txt"""
    config = {}
    if os.path.exists("config.txt"):
        with open("config.txt", 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key.strip()] = value.strip()
    return config

def test_email_connection():
    """Test email connection and send a test email."""
    print("Testing Email Configuration...")
    print("=" * 50)
    
    # Load config
    config = load_config()
    
    # Check required settings
    required = ['email', 'app_password']
    missing = [key for key in required if not config.get(key)]
    
    if missing:
        print(f"❌ Missing required settings: {', '.join(missing)}")
        print("Please update config.txt with your email settings.")
        return False
    
    # Test SMTP connection
    try:
        print("Testing SMTP connection...")
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['email'], config['app_password'])
        print("SUCCESS: SMTP connection successful!")
        
        # Send test email to yourself
        print("Sending test email to yourself...")
        
        msg = MIMEMultipart()
        msg['From'] = config['email']
        msg['To'] = config['email']  # Send to yourself
        msg['Subject'] = "Email Automation Test"
        
        body = """
        This is a test email from your Email Automation Script.
        
        If you received this email, your configuration is working correctly!
        
        You can now run the full automation script.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server.send_message(msg)
        print("SUCCESS: Test email sent successfully!")
        
        server.quit()
        print("Disconnected from SMTP server")
        
        print("\nAll tests passed! Your email configuration is working.")
        print("You can now run the main script with: python send_cv.py")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Authentication failed!")
        print("Please check your Gmail App Password in config.txt")
        print("Make sure you're using the App Password, not your regular Gmail password.")
        return False
        
    except smtplib.SMTPException as e:
        print(f"ERROR: SMTP error: {e}")
        return False
        
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False

def check_files():
    """Check if all required files exist."""
    print("Checking required files...")
    
    required_files = [
        "config.txt",
        "recipients.csv", 
        "send_cv.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"FOUND: {file}")
    
    if missing_files:
        print(f"ERROR: Missing files: {', '.join(missing_files)}")
        return False
    
    print("SUCCESS: All required files found!")
    return True

def check_recipients():
    """Check recipients.csv format."""
    print("Checking recipients.csv...")
    
    if not os.path.exists("recipients.csv"):
        print("ERROR: recipients.csv not found")
        return False
    
    try:
        import csv
        with open("recipients.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if not rows:
                print("ERROR: No recipients found in CSV")
                return False
            
            # Check required columns
            required_columns = ['email', 'name', 'company']
            missing_columns = [col for col in required_columns if col not in reader.fieldnames]
            
            if missing_columns:
                print(f"ERROR: Missing columns in CSV: {', '.join(missing_columns)}")
                return False
            
            print(f"SUCCESS: Found {len(rows)} recipients")
            print("SUCCESS: CSV format is correct")
            return True
            
    except Exception as e:
        print(f"ERROR: Error reading CSV: {e}")
        return False

def main():
    """Main test function."""
    print("Email Automation - Configuration Test")
    print("=" * 50)
    
    # Check files
    if not check_files():
        return
    
    # Check recipients
    if not check_recipients():
        return
    
    # Test email
    if test_email_connection():
        print("\nEverything looks good! You're ready to run the automation.")
    else:
        print("\nPlease fix the issues above before running the automation.")

if __name__ == "__main__":
    main()
