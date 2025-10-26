#!/usr/bin/env python3
"""
Streamlit Email Automation Web App
A web-based interface for sending personalized job application emails with attachments.
Based on the original send_cv.py script with enhanced UI and security features.
"""

import streamlit as st
import smtplib
import csv
import time
import random
import logging
import os
import tempfile
import pandas as pd
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict
import io
import re
import json
import hashlib

# Configure Streamlit page
st.set_page_config(
    page_title="Email Automation App",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class EmailAutomation:
    """
    Email automation class - enhanced with configurable templates and settings.
    """
    def __init__(self, config: Dict):
        """Initialize the email automation with configuration."""
        self.config = config
        self.server = None
        self.sent_count = 0
        self.failed_count = 0
        
    def get_random_subject(self) -> str:
        """Get a random subject line variation."""
        subjects = self.config.get('subjects', [
            "Candidature pour un stage PFE – Développement web / IA / Data / Testing",
            "Candidature stage PFE - Développement web / IA / Data / Testing",
            "Candidature pour stage PFE - Technologies numériques",
            "Candidature spontanée - Stage PFE Développement / IA / Data",
            "Candidature pour un stage PFE - Développement et Intelligence Artificielle"
        ])
        return random.choice(subjects)
    
    def get_random_greeting(self, name: str) -> str:
        """Get a consistent greeting for personalized feel."""
        greetings = self.config.get('greetings', ["Bonjour", "Salut", "Bonjour"])
        greeting = random.choice(greetings)
        if not name:
            return f"{greeting},"
        return f"{greeting} {name},"
    
    def create_html_email(self, name: str, company: str) -> str:
        """Create a professional HTML email template using configurable content."""
        template_config = self.config.get('template', {})
        
        # Check if using custom template
        if template_config.get('is_custom', False):
            return self.create_custom_html_email(name, company)
        
        # Use pre-built architecture
        greeting = self.get_random_greeting(name)
        company_sentence = (f" au sein de <strong>{company}</strong>" if company else "")
        
        # Get configurable template content
        html_template = template_config.get('html', self.get_default_html_template())
        
        # Replace placeholders
        html_content = html_template.format(
            greeting=greeting,
            company_sentence=company_sentence,
            sender_name=template_config.get('sender_name', 'Othmane Chaikhi'),
            sender_title=template_config.get('sender_title', 'étudiant en cycle ingénieur en Informatique et Réseaux (MIAGE) à l\'EMSI Rabat (2023–2026)'),
            projects=template_config.get('projects', self.get_default_projects()),
            objective=template_config.get('objective', 'Mon objectif est de mettre en pratique mes compétences techniques, d\'apprendre auprès de professionnels expérimentés et de contribuer à vos projets innovants dans le domaine du numérique.'),
            closing=template_config.get('closing', 'Je vous remercie sincèrement pour votre temps et votre considération.'),
            signature_name=template_config.get('signature_name', 'Othmane Chaikhi'),
            phone=template_config.get('phone', '+212 631-889579'),
            email=self.config['email'],
            website=template_config.get('website', 'https://othmanechaikhi.page.gd')
        )
        
        return html_content
    
    def create_custom_html_email(self, name: str, company: str) -> str:
        """Create HTML email using custom template."""
        template_config = self.config.get('template', {})
        html_template = template_config.get('html', '')
        
        if not html_template:
            st.warning("No custom HTML template found. Using default template.")
            return self.get_default_html_template()
        
        # Replace variables in custom template
        greeting = self.get_random_greeting(name)
        
        # Use smart formatting that handles CSS vs template variables
        return smart_format_template(
            html_template,
            name=name or '',
            company=company or '',
            email=self.config.get('email', ''),
            greeting=greeting
        )
    
    def get_default_html_template(self) -> str:
        """Default HTML template."""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
        .content {{ padding: 20px 0; }}
        .footer {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }}
        .signature {{ margin-top: 20px; }}
        .highlight {{ background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        ul {{ margin: 10px 0; padding-left: 20px; }}
        li {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2 style="color: #007bff; margin: 0;">Candidature Stage PFE</h2>
        </div>
        
        <div class="content">
            <p>{greeting}</p>
            
            <p>Je me permets de vous contacter afin de vous présenter ma candidature pour un stage de fin d'études (PFE) en développement web, intelligence artificielle, data ou testing{company_sentence}.</p>
            
            <div class="highlight">
                <p><strong>Je m'appelle {sender_name}</strong>, {sender_title}.</p>
                <p>Passionné par le développement et les technologies émergentes, j'ai réalisé plusieurs projets académiques et freelances, notamment :</p>
                <ul>
                    {projects}
                </ul>
            </div>
            
            <p>{objective}</p>
            
            <p>Vous trouverez ci-joint mon CV, que j'espère retiendra votre attention.<br>
            Je serais honoré de pouvoir échanger avec vous au sujet de cette opportunité de stage.</p>
            
            <p>{closing}</p>
        </div>
        
        <div class="footer">
            <div class="signature">
                <p><strong>Bien cordialement,</strong><br>
                <strong>{signature_name}</strong><br>
                📞 {phone}<br>
                📧 {email}</p>
                <p>🔗 <a href="{website}" target="_blank">{website}</a></p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def get_default_projects(self) -> str:
        """Default projects list."""
        return """
        <li>une application e-commerce complète (Django, SEO) pour une coopérative marocaine,</li>
        <li>un tableau de bord RH (Power BI, analyse de données),</li>
        <li>des applications web avec Spring Boot, Java EE et Django,</li>
        <li>et des projets d'IA utilisant Python, machine learning et visualisation de données.</li>
        """
    
    def create_text_email(self, name: str, company: str) -> str:
        """Create a plain text email template using configurable content."""
        template_config = self.config.get('template', {})
        
        # Check if using custom template
        if template_config.get('is_custom', False):
            return self.create_custom_text_email(name, company)
        
        # Use pre-built architecture
        greeting = self.get_random_greeting(name)
        company_sentence = (f" au sein de {company}" if company else "")
        
        # Get configurable template content
        text_template = template_config.get('text', self.get_default_text_template())
        
        # Replace placeholders
        text_content = text_template.format(
            greeting=greeting,
            company_sentence=company_sentence,
            sender_name=template_config.get('sender_name', 'Othmane Chaikhi'),
            sender_title=template_config.get('sender_title', 'étudiant en cycle ingénieur en Informatique et Réseaux (MIAGE) à l\'EMSI Rabat (2023–2026)'),
            projects=template_config.get('projects_text', self.get_default_projects_text()),
            objective=template_config.get('objective', 'Mon objectif est de mettre en pratique mes compétences techniques, d\'apprendre auprès de professionnels expérimentés et de contribuer à vos projets innovants dans le domaine du numérique.'),
            closing=template_config.get('closing', 'Je vous remercie sincèrement pour votre temps et votre considération.'),
            signature_name=template_config.get('signature_name', 'Othmane Chaikhi'),
            phone=template_config.get('phone', '+212 631-889579'),
            email=self.config['email'],
            website=template_config.get('website', 'https://othmanechaikhi.page.gd')
        )
        
        return text_content.strip()
    
    def create_custom_text_email(self, name: str, company: str) -> str:
        """Create text email using custom template."""
        template_config = self.config.get('template', {})
        text_template = template_config.get('text', '')
        
        if not text_template:
            st.warning("No custom text template found. Using default template.")
            return self.get_default_text_template()
        
        # Replace variables in custom template
        greeting = self.get_random_greeting(name)
        
        # Use smart formatting that handles CSS vs template variables
        return smart_format_template(
            text_template,
            name=name or '',
            company=company or '',
            email=self.config.get('email', ''),
            greeting=greeting
        ).strip()
    
    def get_default_text_template(self) -> str:
        """Default text template."""
        return """
{greeting}

Je me permets de vous contacter afin de vous présenter ma candidature pour un stage de fin d'études (PFE) en développement web, intelligence artificielle, data ou testing{company_sentence}.

Je m'appelle {sender_name}, {sender_title}.
Passionné par le développement et les technologies émergentes, j'ai réalisé plusieurs projets académiques et freelances, notamment :

{projects}

{objective}

Vous trouverez ci-joint mon CV, que j'espère retiendra votre attention.
Je serais honoré de pouvoir échanger avec vous au sujet de cette opportunité de stage.

{closing}

Bien cordialement,
{signature_name}
📞 {phone}
📧 {email}

🔗 {website}
        """
    
    def get_default_projects_text(self) -> str:
        """Default projects list for text."""
        return """- une application e-commerce complète (Django, SEO) pour une coopérative marocaine,
- un tableau de bord RH (Power BI, analyse de données),
- des applications web avec Spring Boot, Java EE et Django,
- et des projets d'IA utilisant Python, machine learning et visualisation de données."""
    
    def connect_smtp(self) -> bool:
        """Connect to SMTP server."""
        try:
            self.server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            self.server.starttls()
            self.server.login(self.config['email'], self.config['app_password'])
            return True
        except Exception as e:
            st.error(f"Failed to connect to SMTP: {e}")
            return False
    
    def send_email(self, recipient: Dict, cv_path: str) -> bool:
        """Send a single email to a recipient."""
        try:
            # Create main message container
            msg = MIMEMultipart('mixed')
            msg['From'] = self.config['email']
            msg['To'] = recipient.get('email', '')
            msg['Subject'] = self.get_random_subject()
            
            # Create alternative container for text and HTML
            alternative = MIMEMultipart('alternative')
            
            # Create text and HTML versions
            name = recipient.get('name', '') or ''
            company = recipient.get('company', '') or ''

            text_content = self.create_text_email(name, company)
            html_content = self.create_html_email(name, company)
            
            # Attach both versions to alternative container
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')
            
            alternative.attach(text_part)
            alternative.attach(html_part)
            
            # Attach the alternative container to main message
            msg.attach(alternative)
            
            # Attach CV if it exists
            if os.path.exists(cv_path):
                with open(cv_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(cv_path)}'
                    )
                    msg.attach(part)
            
            # Send email
            self.server.send_message(msg)
            self.sent_count += 1
            return True
            
        except Exception as e:
            self.failed_count += 1
            st.error(f"Failed to send to {recipient['email']}: {e}")
            return False

def validate_email(email: str) -> bool:
    """Simple email validation."""
    return '@' in email and '.' in email.split('@')[1]

def check_admin_access():
    """Check if user has admin access to saved recipients."""
    # Load admin password from config file
    admin_password = "admin123"  # Default password
    
    try:
        if os.path.exists("admin_config.txt"):
            with open("admin_config.txt", 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('admin_password='):
                        admin_password = line.split('=', 1)[1].strip()
                        break
    except Exception:
        pass  # Use default password if config file can't be read
    
    if 'admin_authenticated' not in st.session_state:
        st.session_state['admin_authenticated'] = False
    
    if not st.session_state['admin_authenticated']:
        with st.sidebar:
            st.markdown("---")
            st.subheader("🔐 Admin Access")
            entered_password = st.text_input("Enter admin password:", type="password", key="admin_password")
            
            if st.button("Login", key="admin_login"):
                if entered_password == admin_password:
                    st.session_state['admin_authenticated'] = True
                    st.success("✅ Admin access granted!")
                    st.rerun()
                else:
                    st.error("❌ Invalid password")
            
            return False
    
    return True

def logout_admin():
    """Logout admin user."""
    st.session_state['admin_authenticated'] = False
    st.rerun()

def safe_format_template(template: str, **kwargs) -> str:
    """Safely format a template with error handling."""
    try:
        return template.format(**kwargs)
    except KeyError as e:
        st.error(f"Template error: Variable {e} not found in template")
        return f"Template Error: Variable {e} not found in template.\n\n{template}"
    except Exception as e:
        st.error(f"Template error: {e}")
        return f"Template Error: {e}\n\n{template}"

def smart_format_template(template: str, **kwargs) -> str:
    """Smart template formatting that handles CSS vs template variables."""
    import re
    
    # First, ensure CSS is properly formatted
    # Fix any CSS properties that might have spacing issues
    template = re.sub(r'(\w+)\s*:\s*', r'\1:', template)
    
    # Now format the template, but be very careful with CSS
    try:
        # Create a list of valid template variables
        valid_vars = set(kwargs.keys())
        
        # Find all template variables in the template (outside of style blocks)
        # We need to be very careful not to touch CSS properties
        
        # First, protect style blocks by temporarily replacing them
        style_blocks = []
        def protect_style_block(match):
            style_blocks.append(match.group(0))
            return f"__STYLE_BLOCK_{len(style_blocks)-1}__"
        
        # Protect <style> blocks
        protected_template = re.sub(r'<style>.*?</style>', protect_style_block, template, flags=re.DOTALL)
        
        # Protect inline styles
        inline_styles = []
        def protect_inline_style(match):
            inline_styles.append(match.group(0))
            return f"__INLINE_STYLE_{len(inline_styles)-1}__"
        
        protected_template = re.sub(r'style="[^"]*"', protect_inline_style, protected_template)
        
        # Now find and replace template variables in the protected template
        template_vars = re.findall(r'\{([^}]+)\}', protected_template)
        
        result = protected_template
        for var in template_vars:
            if var in valid_vars:
                result = result.replace(f'{{{var}}}', str(kwargs[var]))
        
        # Restore style blocks
        for i, style_block in enumerate(style_blocks):
            result = result.replace(f"__STYLE_BLOCK_{i}__", style_block)
        
        # Restore inline styles
        for i, inline_style in enumerate(inline_styles):
            result = result.replace(f"__INLINE_STYLE_{i}__", inline_style)
        
        return result
        
    except Exception as e:
        st.error(f"Smart template formatting error: {e}")
        return template

def clean_template(template: str) -> str:
    """Clean template to remove problematic formatting."""
    if not template:
        return template
    
    # Remove any leading/trailing whitespace that might cause issues
    template = template.strip()
    
    import re
    
    # NEW APPROACH: Don't escape CSS properties, just ensure they're properly formatted
    # The issue is that CSS properties are being treated as template variables
    # We need to keep CSS working but prevent template variable conflicts
    
    # 1. Fix CSS properties that have spaces before the colon
    # This handles cases like "max-width :" which should be "max-width:"
    template = re.sub(r'(\w+)\s*:\s*', r'\1:', template)
    
    # 2. Ensure CSS properties are properly formatted
    # Handle cases where CSS properties might be malformed
    css_properties = [
        'font-family', 'line-height', 'color', 'max-width', 'margin', 'padding',
        'background-color', 'border-radius', 'text-decoration', 'border',
        'width', 'height', 'font-size', 'font-weight', 'text-align',
        'display', 'position', 'top', 'left', 'right', 'bottom',
        'z-index', 'opacity', 'transform', 'transition', 'animation'
    ]
    
    # Fix spacing issues in CSS properties
    for prop in css_properties:
        # Fix "property :" to "property:"
        template = re.sub(r'\b' + prop + r'\s*:\s*', prop + ':', template)
        # Fix "property :" to "property:"
        template = re.sub(r'\{\s*' + prop + r'\s*:', '{' + prop + ':', template)
    
    return template

def save_recipient_to_file(recipient: Dict):
    """Save a recipient to the saved recipients file."""
    try:
        saved_file = "saved_recipients.json"
        recipients = []
        
        # Load existing recipients
        if os.path.exists(saved_file):
            with open(saved_file, 'r', encoding='utf-8') as f:
                recipients = json.load(f)
        
        # Add new recipient if not already exists
        email = recipient.get('email', '').lower()
        if not any(r.get('email', '').lower() == email for r in recipients):
            recipient['saved_date'] = datetime.now().isoformat()
            recipients.append(recipient)
            
            # Save back to file
            with open(saved_file, 'w', encoding='utf-8') as f:
                json.dump(recipients, f, indent=2, ensure_ascii=False)
            
            return True
        return False
    except Exception as e:
        st.error(f"Error saving recipient: {e}")
        return False

def load_saved_recipients() -> List[Dict]:
    """Load saved recipients from file."""
    try:
        saved_file = "saved_recipients.json"
        if os.path.exists(saved_file):
            with open(saved_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Error loading saved recipients: {e}")
        return []

def delete_saved_recipient(email: str):
    """Delete a recipient from saved recipients."""
    try:
        saved_file = "saved_recipients.json"
        if os.path.exists(saved_file):
            with open(saved_file, 'r', encoding='utf-8') as f:
                recipients = json.load(f)
            
            # Remove recipient
            recipients = [r for r in recipients if r.get('email', '').lower() != email.lower()]
            
            # Save back
            with open(saved_file, 'w', encoding='utf-8') as f:
                json.dump(recipients, f, indent=2, ensure_ascii=False)
            
            return True
        return False
    except Exception as e:
        st.error(f"Error deleting recipient: {e}")
        return False

def parse_text_form_recipients(text: str) -> List[Dict]:
    """Parse recipients from text form (copy/paste)."""
    recipients = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Try to extract email and name from various formats
        # Format 1: email@domain.com
        # Format 2: Name <email@domain.com>
        # Format 3: Name, email@domain.com
        # Format 4: email@domain.com, Name
        
        email = ""
        name = ""
        
        # Check for <email> format
        if '<' in line and '>' in line:
            email_match = re.search(r'<([^>]+)>', line)
            if email_match:
                email = email_match.group(1).strip()
                name = line.replace(f'<{email}>', '').strip()
        else:
            # Try to find email in the line
            email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
            if email_match:
                email = email_match.group(0)
                # Extract name (everything except the email)
                name = line.replace(email, '').strip()
                # Clean up name (remove commas, extra spaces)
                name = re.sub(r'[,;]+', '', name).strip()
        
        if email and validate_email(email):
            recipients.append({
                'email': email,
                'name': name,
                'company': ''  # Default empty company
            })
    
    return recipients

def load_recipients_from_csv(csv_content: str) -> List[Dict]:
    """Load recipients from CSV content."""
    recipients = []
    try:
        # Use StringIO to read CSV from string
        csv_io = io.StringIO(csv_content)
        
        # Try to detect if there's a header
        sample = csv_io.read(2048)
        csv_io.seek(0)
        
        if 'email' in sample.lower().splitlines()[0]:
            # Has header
            reader = csv.DictReader(csv_io)
            for row in reader:
                email = (row.get('email') or row.get('Email') or '').strip()
                name = (row.get('name') or row.get('Name') or '').strip()
                company = (row.get('company') or row.get('Company') or '').strip()
                
                if not email:
                    # Try to find any field that looks like an email
                    for v in row.values():
                        if v and '@' in v:
                            email = v.strip()
                            break
                
                if email and validate_email(email):
                    recipients.append({'email': email, 'name': name, 'company': company})
        else:
            # No header - treat as simple CSV
            reader = csv.reader(csv_io)
            for row in reader:
                if not row:
                    continue
                row = [col.strip() for col in row]
                email = row[0] if row and row[0] else ''
                name = row[1] if len(row) > 1 else ''
                company = row[2] if len(row) > 2 else ''
                
                if '@' not in email:
                    for col in row:
                        if '@' in col:
                            email = col
                            break
                
                if email and validate_email(email):
                    recipients.append({'email': email, 'name': name, 'company': company})
                    
    except Exception as e:
        st.error(f"Error loading recipients: {e}")
    
    return recipients

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">📧 Email Automation App</h1>', unsafe_allow_html=True)
    
    # Check admin access
    is_admin = check_admin_access()
    
    # Show admin info in sidebar
    if is_admin:
        with st.sidebar:
            st.markdown("---")
            st.success("🔐 **Admin Access Granted**")
            st.info("You can access saved recipients and admin features.")
    
    # Create tabs for different sections
    if is_admin:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📧 Email Settings", "📝 Template Editor", "📁 Recipients", "💾 Saved Recipients", "🚀 Send Emails"])
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["📧 Email Settings", "📝 Template Editor", "📁 Recipients", "🚀 Send Emails"])
    
    with tab1:
        st.header("📧 Email Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gmail Settings")
            email = st.text_input("Gmail Address", placeholder="your.email@gmail.com", key="email_input")
            app_password = st.text_input("App Password", type="password", placeholder="Your 16-character app password", key="app_password")
            
            st.subheader("SMTP Settings")
            smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com", help="SMTP server address")
            smtp_port = st.number_input("SMTP Port", value=587, min_value=1, max_value=65535, help="SMTP server port")
        
        with col2:
            st.subheader("Timing Settings")
            min_delay = st.slider("Minimum Delay (seconds)", 10, 120, 40, help="Minimum time between emails")
            max_delay = st.slider("Maximum Delay (seconds)", 30, 300, 90, help="Maximum time between emails")
            
            st.subheader("Safety Limits")
            max_emails = st.slider("Max Emails Per Day", 5, 100, 30, help="Maximum emails to send in one session")
            
            st.subheader("Email Subjects")
            st.text_area("Subject Lines (one per line)", 
                        value="Candidature pour un stage PFE – Développement web / IA / Data / Testing\nCandidature stage PFE - Développement web / IA / Data / Testing\nCandidature pour stage PFE - Technologies numériques\nCandidature spontanée - Stage PFE Développement / IA / Data\nCandidature pour un stage PFE - Développement et Intelligence Artificielle",
                        height=100, key="subjects_input")
        
        # Disclaimer
        st.markdown("---")
        st.markdown("""
        <div class="warning-box">
        <strong>⚠️ Important:</strong><br>
        • Use responsibly and respect email laws<br>
        • Don't exceed Gmail's sending limits<br>
        • Test with small batches first<br>
        • Credentials are not stored permanently
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.header("📝 Email Template Editor")
        
        # Initialize template_config
        template_config = {}
        
        # Template type selection
        st.subheader("🎨 Choose Template Type")
        template_type = st.radio(
            "Select template approach:",
            ["🏗️ Use Pre-built Architecture (Recommended)", "🎨 Create Custom Template"],
            key="template_type_radio"
        )
        
        if template_type == "🏗️ Use Pre-built Architecture (Recommended)":
            st.info("💡 **Pre-built Architecture**: Use our structured template with customizable fields for professional job application emails.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Personal Information")
                template_config['sender_name'] = st.text_input("Your Name", value="Othmane Chaikhi", key="sender_name")
                template_config['sender_title'] = st.text_area("Your Title/Position", 
                    value="étudiant en cycle ingénieur en Informatique et Réseaux (MIAGE) à l'EMSI Rabat (2023–2026)",
                    height=60, key="sender_title")
                template_config['phone'] = st.text_input("Phone Number", value="+212 631-889579", key="phone")
                template_config['website'] = st.text_input("Website/Portfolio", value="https://othmanechaikhi.page.gd", key="website")
                
                st.subheader("Greetings")
                greetings_text = st.text_area("Greeting Options (one per line)", 
                    value="Bonjour\nSalut\nBonjour", 
                    height=80, key="greetings_input")
            
            with col2:
                st.subheader("Email Content")
                template_config['objective'] = st.text_area("Your Objective", 
                    value="Mon objectif est de mettre en pratique mes compétences techniques, d'apprendre auprès de professionnels expérimentés et de contribuer à vos projets innovants dans le domaine du numérique.",
                    height=80, key="objective")
                template_config['closing'] = st.text_area("Closing Message", 
                    value="Je vous remercie sincèrement pour votre temps et votre considération.",
                    height=60, key="closing")
                template_config['signature_name'] = st.text_input("Signature Name", value="Othmane Chaikhi", key="signature_name")
                
                st.subheader("Projects")
                projects_text = st.text_area("Your Projects (one per line)", 
                    value="une application e-commerce complète (Django, SEO) pour une coopérative marocaine\nun tableau de bord RH (Power BI, analyse de données)\ndes applications web avec Spring Boot, Java EE et Django\net des projets d'IA utilisant Python, machine learning et visualisation de données",
                    height=120, key="projects_input")
        
            # Preview section
            st.markdown("---")
            st.subheader("📄 Email Preview")
            
            if st.button("🔄 Generate Preview", key="preview_btn"):
                # Create preview configuration
                preview_config = {
                    'email': email or 'your.email@example.com',
                    'template': template_config,
                    'subjects': [line.strip() for line in st.session_state.get('subjects_input', '').split('\n') if line.strip()],
                    'greetings': [line.strip() for line in st.session_state.get('greetings_input', '').split('\n') if line.strip()]
                }
                
                # Generate projects HTML
                projects_html = ""
                projects_list = [line.strip() for line in st.session_state.get('projects_input', '').split('\n') if line.strip()]
                for project in projects_list:
                    projects_html += f"<li>{project}</li>\n"
                
                preview_config['template']['projects'] = projects_html
                preview_config['template']['projects_text'] = '\n'.join([f"- {project}" for project in projects_list])
                
                # Create automation instance for preview
                automation = EmailAutomation(preview_config)
                
                # Generate sample email
                sample_name = "John Doe"
                sample_company = "Tech Company"
                
                # Show HTML preview
                html_content = automation.create_html_email(sample_name, sample_company)
                st.markdown("**HTML Preview:**")
                st.components.v1.html(html_content, height=600, scrolling=True)
                
                # Show text preview
                text_content = automation.create_text_email(sample_name, sample_company)
                st.markdown("**Text Preview:**")
                st.text_area("Plain Text Version", text_content, height=300, disabled=True)
        
        else:  # Custom Template
            st.info("🎨 **Custom Template**: Create your own email template from scratch with full control over content and formatting.")
            
            # Custom template editor
            st.subheader("📝 Custom Template Editor")
            
            # Template format selection
            template_format = st.radio(
                "Choose template format:",
                ["📄 HTML Template", "📝 Text Template", "🔄 Both HTML & Text"],
                key="custom_template_format"
            )
            
            # Initialize custom template in session state
            if 'custom_html_template' not in st.session_state:
                st.session_state['custom_html_template'] = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
        .content {{ padding: 20px 0; }}
        .footer {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Your Email Subject</h2>
        </div>
        <div class="content">
            <p>Dear {name},</p>
            <p>Your custom email content here...</p>
            <p>You can use variables like {name}, {company}, {email} in your template.</p>
        </div>
        <div class="footer">
            <p>Best regards,<br>Your Name</p>
        </div>
    </div>
</body>
</html>"""
            
            # FORCE clean templates on every load to prevent issues
            if 'custom_html_template' in st.session_state:
                current_template = st.session_state['custom_html_template']
                # Force clean with multiple passes
                cleaned_template = clean_template(current_template)
                cleaned_template = clean_template(cleaned_template)
                cleaned_template = clean_template(cleaned_template)  # Triple pass for safety
                st.session_state['custom_html_template'] = cleaned_template
                if current_template != cleaned_template:
                    st.info("🔧 **Template automatically cleaned to fix CSS conflicts.**")
            
            if 'custom_text_template' in st.session_state:
                current_template = st.session_state['custom_text_template']
                # Force clean with multiple passes
                cleaned_template = clean_template(current_template)
                cleaned_template = clean_template(cleaned_template)
                cleaned_template = clean_template(cleaned_template)  # Triple pass for safety
                st.session_state['custom_text_template'] = cleaned_template
            
            # Add template management buttons
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                if st.button("🔄 Reset Template", key="reset_custom_template"):
                    # Clear all template-related session state
                    if 'custom_html_template' in st.session_state:
                        del st.session_state['custom_html_template']
                    if 'custom_text_template' in st.session_state:
                        del st.session_state['custom_text_template']
                    
                    # Force clear and reinitialize
                    st.session_state['custom_html_template'] = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
        .content {{ padding: 20px 0; }}
        .footer {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Your Email Subject</h2>
        </div>
        <div class="content">
            <p>Dear {name},</p>
            <p>Your custom email content here...</p>
            <p>You can use variables like {name}, {company}, {email} in your template.</p>
        </div>
        <div class="footer">
            <p>Best regards,<br>Your Name</p>
        </div>
    </div>
</body>
</html>"""
                    st.session_state['custom_text_template'] = """Dear {name},

Your custom email content here...

You can use variables like {name}, {company}, {email} in your template.

Best regards,
Your Name"""
                    st.success("✅ Templates reset to defaults!")
                    st.rerun()
            
            with col3:
                if st.button("🔧 Fix Template", key="fix_custom_template"):
                    # Clean the current template in session state
                    if 'custom_html_template' in st.session_state:
                        current_template = st.session_state['custom_html_template']
                        # Multiple cleaning passes
                        cleaned_template = clean_template(current_template)
                        cleaned_template = clean_template(cleaned_template)
                        cleaned_template = clean_template(cleaned_template)
                        st.session_state['custom_html_template'] = cleaned_template
                        st.success("✅ HTML template cleaned and fixed!")
                        
                        # Show what was changed
                        if current_template != cleaned_template:
                            st.info("🔍 **Template was automatically cleaned to fix CSS property conflicts.**")
                            # Show debug info
                            with st.expander("🔍 Debug: Show template changes"):
                                st.code("BEFORE:\n" + current_template, language='html')
                                st.code("AFTER:\n" + cleaned_template, language='html')
                    
                    if 'custom_text_template' in st.session_state:
                        current_template = st.session_state['custom_text_template']
                        # Multiple cleaning passes
                        cleaned_template = clean_template(current_template)
                        cleaned_template = clean_template(cleaned_template)
                        cleaned_template = clean_template(cleaned_template)
                        st.session_state['custom_text_template'] = cleaned_template
                        st.success("✅ Text template cleaned and fixed!")
                    
                    st.rerun()
            
            if 'custom_text_template' not in st.session_state:
                st.session_state['custom_text_template'] = """Dear {name},

Your custom email content here...

You can use variables like {name}, {company}, {email} in your template.

Best regards,
Your Name"""
            
            # HTML Template Editor
            if template_format in ["📄 HTML Template", "🔄 Both HTML & Text"]:
                st.subheader("📄 HTML Template")
                st.markdown("**Available variables:** `{name}`, `{company}`, `{email}`, `{greeting}`")
                
                html_template = st.text_area(
                    "HTML Template:",
                    value=st.session_state['custom_html_template'],
                    height=400,
                    key="custom_html_editor",
                    help="Write your HTML email template. Use variables like {name}, {company} for personalization."
                )
                st.session_state['custom_html_template'] = html_template
            
            # Text Template Editor
            if template_format in ["📝 Text Template", "🔄 Both HTML & Text"]:
                st.subheader("📝 Text Template")
                st.markdown("**Available variables:** `{name}`, `{company}`, `{email}`, `{greeting}`")
                
                text_template = st.text_area(
                    "Text Template:",
                    value=st.session_state['custom_text_template'],
                    height=300,
                    key="custom_text_editor",
                    help="Write your plain text email template. Use variables like {name}, {company} for personalization."
                )
                st.session_state['custom_text_template'] = text_template
            
            # Custom template preview
            st.markdown("---")
            st.subheader("📄 Custom Template Preview")
            
            if st.button("🔄 Generate Custom Preview", key="custom_preview_btn"):
                # Create preview configuration for custom template
                custom_config = {
                    'email': email or 'your.email@example.com',
                    'template': {
                        'html': st.session_state.get('custom_html_template', ''),
                        'text': st.session_state.get('custom_text_template', ''),
                        'is_custom': True
                    },
                    'subjects': [line.strip() for line in st.session_state.get('subjects_input', '').split('\n') if line.strip()],
                    'greetings': [line.strip() for line in st.session_state.get('greetings_input', '').split('\n') if line.strip()]
                }
                
                # Generate sample email with custom template
                sample_name = "John Doe"
                sample_company = "Tech Company"
                sample_email = "john@example.com"
                
                # Show HTML preview
                if template_format in ["📄 HTML Template", "🔄 Both HTML & Text"]:
                    html_template = st.session_state.get('custom_html_template', '')
                    if html_template:
                        html_content = smart_format_template(
                            html_template,
                            name=sample_name,
                            company=sample_company,
                            email=sample_email,
                            greeting=f"Dear {sample_name}"
                        )
                        st.markdown("**HTML Preview:**")
                        st.components.v1.html(html_content, height=600, scrolling=True)
                        
                        # Debug: Show template content if there's an error
                        if "Template Error:" in html_content:
                            st.markdown("**Debug - Template Content:**")
                            st.code(html_template, language='html')
                        
                        # Debug: Show processed content
                        with st.expander("🔍 Debug: Show processed HTML"):
                            st.code(html_content, language='html')
                        
                        # Debug: Show original template
                        with st.expander("🔍 Debug: Show original template"):
                            st.code(html_template, language='html')
                    else:
                        st.warning("No HTML template found. Please create a template first.")
                
                # Show text preview
                if template_format in ["📝 Text Template", "🔄 Both HTML & Text"]:
                    text_template = st.session_state.get('custom_text_template', '')
                    if text_template:
                        text_content = smart_format_template(
                            text_template,
                            name=sample_name,
                            company=sample_company,
                            email=sample_email,
                            greeting=f"Dear {sample_name}"
                        )
                        st.markdown("**Text Preview:**")
                        st.text_area("Plain Text Version", text_content, height=300, disabled=True)
                    else:
                        st.warning("No text template found. Please create a template first.")
            
            # Custom template instructions
            st.markdown("---")
            st.subheader("💡 Custom Template Instructions")
            st.markdown("""
            **Available Variables:**
            - `{name}` - Recipient's name
            - `{company}` - Recipient's company
            - `{email}` - Recipient's email
            - `{greeting}` - Personalized greeting
            
            **Tips:**
            - Use HTML tags for formatting in HTML template
            - Keep text template simple and readable
            - Test your template with the preview before sending
            - Variables will be automatically replaced with actual recipient data
            """)
    
    with tab3:
        st.header("📁 Recipients & Files")
        
        # CV Upload Section
        st.subheader("📄 Upload CV (PDF)")
        cv_file = st.file_uploader("Upload your CV", type=['pdf'], help="Upload your CV in PDF format", key="cv_upload")
        
        if cv_file:
            st.success(f"✅ CV uploaded: {cv_file.name}")
            # Save CV temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(cv_file.getvalue())
                cv_path = tmp_file.name
        else:
            cv_path = None
            st.warning("⚠️ Please upload your CV")
        
        st.markdown("---")
        
        # Recipients Input Methods
        st.subheader("📋 Add Recipients")
        
        # Toggle between CSV upload and text form
        input_method = st.radio(
            "Choose input method:",
            ["📄 Upload CSV File", "📝 Copy/Paste Text Form"],
            key="input_method"
        )
        
        recipients = []
        
        if input_method == "📄 Upload CSV File":
            st.subheader("📄 Upload Recipients CSV")
            csv_file = st.file_uploader("Upload recipients CSV", type=['csv'], help="CSV with columns: email, name, company", key="csv_upload")
            
            if csv_file:
                st.success(f"✅ CSV uploaded: {csv_file.name}")
                
                # Preview CSV
                try:
                    csv_content = csv_file.read().decode('utf-8')
                    recipients = load_recipients_from_csv(csv_content)
                    
                    if recipients:
                        st.subheader("📊 Recipients Preview")
                        df = pd.DataFrame(recipients)
                        st.dataframe(df, width='stretch')
                        st.info(f"Found {len(recipients)} valid recipients")
                        
                        # Save recipients option (admin only)
                        if is_admin:
                            if st.button("💾 Save these recipients", key="save_csv_recipients"):
                                saved_count = 0
                                for recipient in recipients:
                                    if save_recipient_to_file(recipient):
                                        saved_count += 1
                                st.success(f"✅ Saved {saved_count} recipients to your collection!")
                    else:
                        st.error("No valid recipients found in CSV")
                        
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
                    recipients = []
            else:
                st.warning("⚠️ Please upload recipients CSV")
        
        else:  # Text Form
            st.subheader("📝 Copy/Paste Recipients")
            st.markdown("""
            **Supported formats:**
            - `email@domain.com`
            - `Name <email@domain.com>`
            - `Name, email@domain.com`
            - `email@domain.com, Name`
            """)
            
            text_input = st.text_area(
                "Paste your recipients here (one per line):",
                height=200,
                placeholder="john@example.com\nJane Doe <jane@example.com>\nBob Smith, bob@example.com",
                key="text_recipients"
            )
            
            if text_input.strip():
                recipients = parse_text_form_recipients(text_input)
                
                if recipients:
                    st.subheader("📊 Parsed Recipients")
                    df = pd.DataFrame(recipients)
                    st.dataframe(df, width='stretch')
                    st.info(f"Found {len(recipients)} valid recipients")
                    
                    # Save recipients option (admin only)
                    if is_admin:
                        if st.button("💾 Save these recipients", key="save_text_recipients"):
                            saved_count = 0
                            for recipient in recipients:
                                if save_recipient_to_file(recipient):
                                    saved_count += 1
                            st.success(f"✅ Saved {saved_count} recipients to your collection!")
                else:
                    st.error("No valid recipients found in the text")
            else:
                st.warning("⚠️ Please enter recipients in the text area")
    
    if is_admin:
        with tab4:
            st.header("💾 Saved Recipients (Admin Only)")
            
            # Admin logout option
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🚪 Logout Admin", key="logout_admin"):
                    logout_admin()
            
            # Load saved recipients
            saved_recipients = load_saved_recipients()
            
            if saved_recipients:
                st.subheader(f"📊 Your Saved Recipients ({len(saved_recipients)} total)")
            
                # Display saved recipients
                df = pd.DataFrame(saved_recipients)
                st.dataframe(df, width='stretch')
                
                # Actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🔄 Use All Saved Recipients", key="use_all_saved"):
                        st.session_state['selected_recipients'] = saved_recipients
                        st.success(f"✅ Selected {len(saved_recipients)} recipients for sending!")
                
                with col2:
                    if st.button("📥 Export as CSV", key="export_saved"):
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"saved_recipients_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                
                with col3:
                    if st.button("🗑️ Clear All Saved", key="clear_all_saved"):
                        if os.path.exists("saved_recipients.json"):
                            os.remove("saved_recipients.json")
                        st.success("✅ All saved recipients cleared!")
                        st.rerun()
                
                # Individual recipient management
                st.markdown("---")
                st.subheader("🔧 Manage Individual Recipients")
                
                # Select recipient to manage
                recipient_options = [f"{r.get('name', '')} ({r.get('email', '')})" for r in saved_recipients]
                if recipient_options:
                    selected_recipient = st.selectbox("Select recipient to manage:", recipient_options, key="manage_recipient")
                    
                    if selected_recipient:
                        # Find the selected recipient
                        selected_email = selected_recipient.split('(')[-1].rstrip(')')
                        selected_recipient_data = next((r for r in saved_recipients if r.get('email') == selected_email), None)
                        
                        if selected_recipient_data:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Email:** {selected_recipient_data.get('email')}")
                                st.write(f"**Name:** {selected_recipient_data.get('name', 'N/A')}")
                                st.write(f"**Company:** {selected_recipient_data.get('company', 'N/A')}")
                                st.write(f"**Saved:** {selected_recipient_data.get('saved_date', 'N/A')}")
                            
                            with col2:
                                if st.button("📧 Use This Recipient", key="use_single_recipient"):
                                    st.session_state['selected_recipients'] = [selected_recipient_data]
                                    st.success("✅ Selected recipient for sending!")
                                
                                if st.button("🗑️ Delete This Recipient", key="delete_single_recipient"):
                                    if delete_saved_recipient(selected_email):
                                        st.success("✅ Recipient deleted!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to delete recipient")
            else:
                st.info("💡 No saved recipients yet. Add some recipients in the 'Recipients' tab and save them!")
                
                # Show example of how to save recipients
                st.markdown("---")
                st.subheader("💡 How to Save Recipients")
                st.markdown("""
                1. Go to the **"Recipients"** tab
                2. Upload a CSV file or use the text form
                3. Click **"💾 Save these recipients"** button
                4. Your recipients will be saved here for future use!
                """)
    
    # Send emails tab (tab4 for non-admin, tab5 for admin)
    send_tab = tab5 if is_admin else tab4
    
    with send_tab:
        st.header("🚀 Send Emails")
        
        # Get recipients from current session or saved recipients
        current_recipients = recipients if 'recipients' in locals() else []
        saved_recipients_session = st.session_state.get('selected_recipients', [])
        
        # Combine recipients
        all_recipients = current_recipients + saved_recipients_session
        
        # Remove duplicates based on email
        seen_emails = set()
        unique_recipients = []
        for recipient in all_recipients:
            email = recipient.get('email', '').lower()
            if email not in seen_emails:
                seen_emails.add(email)
                unique_recipients.append(recipient)
        
        # Check if all required fields are provided
        all_ready = (
            email and app_password and 
            cv_file is not None and 
            len(unique_recipients) > 0
        )
        
        if not all_ready:
            st.warning("⚠️ Please complete all required fields in the previous tabs before sending emails")
        else:
            # Validate email format
            if not validate_email(email):
                st.error("❌ Please enter a valid email address")
                all_ready = False
            
            # Check recipient count
            if len(unique_recipients) > max_emails:
                st.warning(f"⚠️ You have {len(unique_recipients)} recipients but limit is {max_emails}")
                if not st.checkbox("Continue anyway (not recommended)"):
                    all_ready = False
            
            # Show recipient summary
            if unique_recipients:
                st.subheader("📊 Recipients Summary")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Recipients", len(unique_recipients))
                with col2:
                    st.metric("Current Recipients", len(current_recipients))
                    st.metric("Saved Recipients", len(saved_recipients_session))
                
                # Show recipients preview
                if st.checkbox("Show recipients preview", key="show_recipients_preview"):
                    df = pd.DataFrame(unique_recipients)
                    st.dataframe(df, width='stretch')
        
        # Send button
        if st.button("🚀 Start Sending Emails", disabled=not all_ready, type="primary", key="send_btn"):
            if all_ready:
                # Create configuration
                config = {
                    'email': email,
                    'app_password': app_password,
                    'smtp_server': smtp_server,
                    'smtp_port': smtp_port,
                    'min_delay': min_delay,
                    'max_delay': max_delay,
                    'max_emails_per_day': max_emails,
                    'subjects': [line.strip() for line in st.session_state.get('subjects_input', '').split('\n') if line.strip()],
                    'greetings': [line.strip() for line in st.session_state.get('greetings_input', '').split('\n') if line.strip()],
                    'template': template_config
                }
                
                # Handle custom template configuration
                if st.session_state.get('template_type_radio') == "🎨 Create Custom Template":
                    custom_template_config = {
                        'is_custom': True,
                        'html': st.session_state.get('custom_html_template', ''),
                        'text': st.session_state.get('custom_text_template', '')
                    }
                    config['template'] = custom_template_config
                
                # Initialize email automation
                automation = EmailAutomation(config)
                
                # Connect to SMTP
                with st.spinner("Connecting to Gmail..."):
                    if not automation.connect_smtp():
                        st.error("❌ Failed to connect to Gmail. Check your credentials.")
                        return
                
                st.success("✅ Connected to Gmail successfully!")
                
                # Create progress containers
                progress_bar = st.progress(0)
                status_text = st.empty()
                results_container = st.container()
                
                # Send emails with progress tracking
                try:
                    total_recipients = len(unique_recipients)
                    
                    for i, recipient in enumerate(unique_recipients):
                        # Update progress
                        progress = (i + 1) / total_recipients
                        progress_bar.progress(progress)
                        
                        # Update status
                        status_text.text(f"Sending email {i+1}/{total_recipients} to {recipient['email']}")
                        
                        # Send email
                        success = automation.send_email(recipient, cv_path)
                        
                        # Show result
                        if success:
                            results_container.success(f"✅ Sent to {recipient['email']}")
                        else:
                            results_container.error(f"❌ Failed to send to {recipient['email']}")
                        
                        # Random delay between emails (except for the last one)
                        if i < total_recipients - 1:
                            delay = random.randint(min_delay, max_delay)
                            status_text.text(f"Waiting {delay}s before next email...")
                            time.sleep(delay)
                    
                    # Final results
                    st.markdown("---")
                    st.markdown("## 📊 Campaign Results")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Recipients", total_recipients)
                    with col2:
                        st.metric("Successfully Sent", automation.sent_count)
                    with col3:
                        st.metric("Failed", automation.failed_count)
                    
                    if automation.sent_count > 0:
                        st.success(f"🎉 Campaign completed! {automation.sent_count} emails sent successfully.")
                    else:
                        st.error("❌ No emails were sent successfully.")
                        
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")
                finally:
                    # Clean up temporary files
                    if cv_path and os.path.exists(cv_path):
                        os.unlink(cv_path)
                    
                    # Disconnect from SMTP
                    if automation.server:
                        automation.server.quit()
                        st.info("🔌 Disconnected from Gmail")

if __name__ == "__main__":
    main()
