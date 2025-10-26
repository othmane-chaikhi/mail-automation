#!/usr/bin/env python3
"""
Migration Script - Old App to New App
Migrates data from the old email automation app to the new one.
"""

import json
import csv
import os
from pathlib import Path
from datetime import datetime

def migrate_config():
    """Migrate configuration from old config files."""
    print("🔄 Migrating configuration...")
    
    # Try to load from old config.txt
    old_config = {}
    if os.path.exists("config.txt"):
        try:
            with open("config.txt", 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        old_config[key.strip()] = value.strip()
        except Exception as e:
            print(f"⚠️ Could not read config.txt: {e}")
    
    # Try to load from old email_config.json
    if os.path.exists("email_config.json"):
        try:
            with open("email_config.json", 'r', encoding='utf-8') as f:
                old_config.update(json.load(f))
        except Exception as e:
            print(f"⚠️ Could not read email_config.json: {e}")
    
    # Create new config
    new_config = {
        "email": old_config.get('email', ''),
        "password": old_config.get('app_password', old_config.get('password', '')),
        "provider": "gmail",
        "smtp_server": old_config.get('smtp_server', 'smtp.gmail.com'),
        "smtp_port": int(old_config.get('smtp_port', 587)),
        "min_delay": int(old_config.get('min_delay', 30)),
        "max_delay": int(old_config.get('max_delay', 60)),
        "max_emails_per_day": int(old_config.get('max_emails_per_day', 50)),
        "subjects": old_config.get('subjects', [
            "Candidature pour un stage PFE – Développement web / IA / Data",
            "Candidature stage PFE - Technologies numériques",
            "Candidature spontanée - Stage PFE Développement / IA",
            "Candidature pour un stage PFE - Intelligence Artificielle"
        ]),
        "greetings": old_config.get('greetings', ["Bonjour", "Salut", "Bonjour"])
    }
    
    # Save new config
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(new_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuration migrated: {new_config['email']}")
    return new_config

def migrate_recipients():
    """Migrate recipients from old files."""
    print("🔄 Migrating recipients...")
    
    recipients = []
    
    # Try to load from old recipients.csv
    if os.path.exists("recipients.csv"):
        try:
            with open("recipients.csv", 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    recipients.append({
                        "email": row.get('email', '').lower(),
                        "name": row.get('name', ''),
                        "company": row.get('company', ''),
                        "position": row.get('position', ''),
                        "added_date": datetime.now().isoformat(),
                        "last_contacted": "",
                        "status": "active",
                        "notes": ""
                    })
        except Exception as e:
            print(f"⚠️ Could not read recipients.csv: {e}")
    
    # Try to load from old recipients.json
    if os.path.exists("recipients.json"):
        try:
            with open("recipients.json", 'r', encoding='utf-8') as f:
                old_recipients = json.load(f)
                for recipient in old_recipients:
                    recipients.append({
                        "email": recipient.get('email', '').lower(),
                        "name": recipient.get('name', ''),
                        "company": recipient.get('company', ''),
                        "position": recipient.get('position', ''),
                        "added_date": recipient.get('added_date', datetime.now().isoformat()),
                        "last_contacted": recipient.get('last_contacted', ''),
                        "status": recipient.get('status', 'active'),
                        "notes": recipient.get('notes', '')
                    })
        except Exception as e:
            print(f"⚠️ Could not read recipients.json: {e}")
    
    # Remove duplicates
    seen_emails = set()
    unique_recipients = []
    for recipient in recipients:
        if recipient['email'] not in seen_emails:
            seen_emails.add(recipient['email'])
            unique_recipients.append(recipient)
    
    # Save new recipients
    with open("recipients.json", 'w', encoding='utf-8') as f:
        json.dump(unique_recipients, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Recipients migrated: {len(unique_recipients)} recipients")
    return unique_recipients

def create_default_templates():
    """Create default email templates."""
    print("🔄 Creating default templates...")
    
    templates = [
        {
            "name": "Stage PFE - HTML",
            "subject": "Candidature pour un stage PFE – Développement web / IA / Data",
            "html_content": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
        .container { max-width: 600px; margin: 0 auto; background: #ffffff; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #f8f9fa; }
        .footer { background: #2c3e50; color: white; padding: 20px; text-align: center; font-size: 12px; }
        .signature { margin-top: 25px; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .highlight { background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0; }
        h1 { margin: 0; font-size: 24px; }
        h2 { color: #2c3e50; margin-top: 0; }
        .contact-info { background: #f1f3f4; padding: 15px; border-radius: 8px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Candidature pour Stage PFE</h1>
        </div>
        <div class="content">
            <p>Bonjour {name},</p>
            
            <p>Je me permets de vous contacter pour vous faire part de mon intérêt pour un stage de fin d'études (PFE) au sein de votre entreprise {company}.</p>
            
            <div class="highlight">
                <p><strong>Mon Profil :</strong></p>
                <ul>
                    <li>Étudiant en dernière année passionné par le développement web</li>
                    <li>Compétences en intelligence artificielle et technologies numériques</li>
                    <li>Expérience dans des projets personnels et académiques</li>
                    <li>Motivé pour contribuer à l'innovation technologique</li>
                </ul>
            </div>
            
            <p>Je serais ravi de pouvoir échanger avec vous sur les opportunités de stage disponibles et de vous présenter mon profil plus en détail.</p>
            
            <p>Je vous remercie sincèrement pour votre temps et votre considération.</p>
            
            <div class="signature">
                <p><strong>Cordialement,</strong><br>
                <strong>Othmane Chaikhi</strong></p>
                <div class="contact-info">
                    <p>📧 Email: {email}<br>
                    📱 Téléphone: +212 631-889579<br>
                    🌐 Portfolio: https://othmanechaikhi.page.gd</p>
                </div>
            </div>
        </div>
        <div class="footer">
            <p>Cette candidature est envoyée dans le cadre de ma recherche de stage PFE</p>
        </div>
    </div>
</body>
</html>""",
            "text_content": """Bonjour {name},

Je me permets de vous contacter pour vous faire part de mon intérêt pour un stage de fin d'études (PFE) au sein de votre entreprise {company}.

MON PROFIL :
- Étudiant en dernière année passionné par le développement web
- Compétences en intelligence artificielle et technologies numériques
- Expérience dans des projets personnels et académiques
- Motivé pour contribuer à l'innovation technologique

Je serais ravi de pouvoir échanger avec vous sur les opportunités de stage disponibles et de vous présenter mon profil plus en détail.

Je vous remercie sincèrement pour votre temps et votre considération.

Cordialement,
Othmane Chaikhi

📧 Email: {email}
📱 Téléphone: +212 631-889579
🌐 Portfolio: https://othmanechaikhi.page.gd

---
Cette candidature est envoyée dans le cadre de ma recherche de stage PFE""",
            "created_date": datetime.now().isoformat(),
            "is_default": True
        }
    ]
    
    # Save templates
    with open("templates.json", 'w', encoding='utf-8') as f:
        json.dump(templates, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Templates created: {len(templates)} templates")
    return templates

def main():
    """Main migration function."""
    print("🚀 Starting migration to Email Automation Pro...")
    print("=" * 60)
    
    # Check if old files exist
    old_files = ["config.txt", "email_config.json", "recipients.csv", "recipients.json"]
    existing_files = [f for f in old_files if os.path.exists(f)]
    
    if existing_files:
        print(f"📁 Found old files: {', '.join(existing_files)}")
    else:
        print("ℹ️ No old files found. Starting with fresh configuration.")
    
    # Migrate configuration
    config = migrate_config()
    
    # Migrate recipients
    recipients = migrate_recipients()
    
    # Create templates
    templates = create_default_templates()
    
    print("=" * 60)
    print("✅ Migration completed successfully!")
    print("")
    print("📧 Email Configuration:")
    print(f"   Email: {config['email']}")
    print(f"   Provider: {config['provider']}")
    print(f"   SMTP: {config['smtp_server']}:{config['smtp_port']}")
    print("")
    print("👥 Recipients:")
    print(f"   Total: {len(recipients)} recipients")
    print(f"   Companies: {len(set(r['company'] for r in recipients if r['company']))}")
    print("")
    print("📝 Templates:")
    print(f"   Total: {len(templates)} templates")
    print("")
    print("🚀 To run the new app:")
    print("   python launch.py")
    print("")
    print("📚 Or with Streamlit directly:")
    print("   streamlit run email_automation.py")
    print("")
    print("📖 Read README.md for full documentation")

if __name__ == "__main__":
    main()
