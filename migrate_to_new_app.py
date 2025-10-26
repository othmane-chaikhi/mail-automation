#!/usr/bin/env python3
"""
Migration Script: Old App to New App
Migrates configuration and recipients from the old app to the new clean app.
"""

import json
import os
import re
from typing import Dict, List

def load_old_config() -> Dict:
    """Load configuration from old config.txt file."""
    config = {}
    try:
        if os.path.exists("config.txt"):
            with open("config.txt", 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
    except Exception as e:
        print(f"⚠️ Could not load old config: {e}")
    return config

def load_old_recipients() -> List[Dict]:
    """Load recipients from old recipients.csv file."""
    import csv
    recipients = []
    try:
        if os.path.exists("recipients.csv"):
            with open("recipients.csv", 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    recipients.append({
                        'email': row.get('email', '').lower(),
                        'name': row.get('name', ''),
                        'company': row.get('company', ''),
                        'added_date': '2024-01-01T00:00:00'  # Default date
                    })
    except Exception as e:
        print(f"⚠️ Could not load old recipients: {e}")
    return recipients

def migrate_config():
    """Migrate configuration from old to new format."""
    print("🔄 Migrating configuration...")
    
    old_config = load_old_config()
    
    new_config = {
        "email": old_config.get('email', ''),
        "app_password": old_config.get('app_password', ''),
        "smtp_server": old_config.get('smtp_server', 'smtp.gmail.com'),
        "smtp_port": int(old_config.get('smtp_port', 587)),
        "min_delay": int(old_config.get('min_delay', 30)),
        "max_delay": int(old_config.get('max_delay', 60)),
        "max_emails_per_day": int(old_config.get('max_emails_per_day', 50)),
        "subjects": [
            "Candidature pour un stage PFE – Développement web / IA / Data",
            "Candidature stage PFE - Technologies numériques",
            "Candidature spontanée - Stage PFE Développement / IA",
            "Candidature pour un stage PFE - Intelligence Artificielle"
        ],
        "greetings": [
            "Bonjour",
            "Salut",
            "Bonjour"
        ]
    }
    
    # Save new config
    with open("email_config.json", 'w', encoding='utf-8') as f:
        json.dump(new_config, f, indent=2, ensure_ascii=False)
    
    print("✅ Configuration migrated successfully!")
    return new_config

def migrate_recipients():
    """Migrate recipients from old to new format."""
    print("🔄 Migrating recipients...")
    
    recipients = load_old_recipients()
    
    # Save new recipients
    with open("recipients.json", 'w', encoding='utf-8') as f:
        json.dump(recipients, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Migrated {len(recipients)} recipients successfully!")
    return recipients

def main():
    """Main migration function."""
    print("🚀 Starting migration from old app to new app...")
    print("=" * 50)
    
    # Check if old files exist
    old_files = ["config.txt", "recipients.csv"]
    existing_files = [f for f in old_files if os.path.exists(f)]
    
    if not existing_files:
        print("ℹ️ No old files found. Starting with fresh configuration.")
        return
    
    print(f"📁 Found old files: {', '.join(existing_files)}")
    
    # Migrate configuration
    if os.path.exists("config.txt"):
        config = migrate_config()
        print(f"📧 Email: {config['email']}")
        print(f"🔑 App password: {'*' * 16}")
        print(f"📡 SMTP: {config['smtp_server']}:{config['smtp_port']}")
    
    # Migrate recipients
    if os.path.exists("recipients.csv"):
        recipients = migrate_recipients()
        print(f"👥 Recipients: {len(recipients)}")
    
    print("=" * 50)
    print("✅ Migration completed successfully!")
    print("")
    print("🚀 To run the new app:")
    print("   python run_app.py")
    print("")
    print("📚 Or with Streamlit directly:")
    print("   streamlit run app_new.py")
    print("")
    print("📖 Read README_NEW.md for full documentation")

if __name__ == "__main__":
    main()
