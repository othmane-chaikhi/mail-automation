"""
Email Automation Pro - Complete Rebuild
A professional email automation system with modern architecture.
"""

import streamlit as st
import smtplib
import ssl
import json
import os
import time
import random
import re
import csv
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Email Automation Pro",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .section-header {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .config-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .button-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .button-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class EmailProvider:
    """Email provider configuration."""
    name: str
    smtp_server: str
    smtp_port: int
    use_tls: bool = True
    use_ssl: bool = False

@dataclass
class EmailConfig:
    """Email configuration data class."""
    email: str
    password: str
    provider: str
    smtp_server: str
    smtp_port: int
    min_delay: int = 30
    max_delay: int = 60
    max_emails_per_day: int = 50
    subjects: List[str] = None
    greetings: List[str] = None
    
    def __post_init__(self):
        if self.subjects is None:
            self.subjects = [
                "Candidature pour un stage PFE – Développement web / IA / Data",
                "Candidature stage PFE - Technologies numériques",
                "Candidature spontanée - Stage PFE Développement / IA",
                "Candidature pour un stage PFE - Intelligence Artificielle"
            ]
        if self.greetings is None:
            self.greetings = ["Bonjour", "Salut", "Bonjour"]

@dataclass
class Recipient:
    """Recipient data class."""
    email: str
    name: str = ""
    company: str = ""
    position: str = ""
    added_date: str = ""
    last_contacted: str = ""
    status: str = "active"
    notes: str = ""
    
    def __post_init__(self):
        if not self.added_date:
            self.added_date = datetime.now().isoformat()

@dataclass
class EmailTemplate:
    """Email template data class."""
    name: str
    subject: str
    html_content: str
    text_content: str
    created_date: str = ""
    is_default: bool = False
    
    def __post_init__(self):
        if not self.created_date:
            self.created_date = datetime.now().isoformat()

class EmailProviders:
    """Email providers configuration."""
    
    PROVIDERS = {
        "gmail": EmailProvider("Gmail", "smtp.gmail.com", 587, True, False),
        "outlook": EmailProvider("Outlook", "smtp-mail.outlook.com", 587, True, False),
        "yahoo": EmailProvider("Yahoo", "smtp.mail.yahoo.com", 587, True, False),
        "custom": EmailProvider("Custom", "", 587, True, False)
    }
    
    @classmethod
    def get_provider(cls, name: str) -> EmailProvider:
        """Get provider configuration."""
        return cls.PROVIDERS.get(name, cls.PROVIDERS["gmail"])
    
    @classmethod
    def get_all_providers(cls) -> Dict[str, EmailProvider]:
        """Get all available providers."""
        return cls.PROVIDERS

class ConfigManager:
    """Configuration management."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.default_config = {
            "email": "",
            "password": "",
            "provider": "gmail",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "min_delay": 30,
            "max_delay": 60,
            "max_emails_per_day": 50,
            "subjects": [
                "Candidature pour un stage PFE – Développement web / IA / Data",
                "Candidature stage PFE - Technologies numériques",
                "Candidature spontanée - Stage PFE Développement / IA",
                "Candidature pour un stage PFE - Intelligence Artificielle"
            ],
            "greetings": ["Bonjour", "Salut", "Bonjour"]
        }
    
    def load_config(self) -> EmailConfig:
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return EmailConfig(**{**self.default_config, **data})
        except Exception as e:
            logger.warning(f"Could not load config: {e}")
        
        return EmailConfig(**self.default_config)
    
    def save_config(self, config: EmailConfig) -> bool:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Could not save config: {e}")
            return False

class RecipientManager:
    """Recipient management."""
    
    def __init__(self, recipients_file: str = "recipients.json"):
        self.recipients_file = Path(recipients_file)
    
    def load_recipients(self) -> List[Recipient]:
        """Load recipients from file."""
        try:
            if self.recipients_file.exists():
                with open(self.recipients_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Recipient(**item) for item in data]
        except Exception as e:
            logger.warning(f"Could not load recipients: {e}")
        return []
    
    def save_recipients(self, recipients: List[Recipient]) -> bool:
        """Save recipients to file."""
        try:
            with open(self.recipients_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(r) for r in recipients], f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Could not save recipients: {e}")
            return False
    
    def add_recipient(self, email: str, name: str = "", company: str = "", 
                     position: str = "", notes: str = "") -> bool:
        """Add a new recipient."""
        recipients = self.load_recipients()
        
        # Check if email already exists
        if any(r.email.lower() == email.lower() for r in recipients):
            return False
        
        new_recipient = Recipient(
            email=email.lower(),
            name=name,
            company=company,
            position=position,
            notes=notes
        )
        
        recipients.append(new_recipient)
        return self.save_recipients(recipients)
    
    def remove_recipient(self, email: str) -> bool:
        """Remove a recipient."""
        recipients = self.load_recipients()
        recipients = [r for r in recipients if r.email.lower() != email.lower()]
        return self.save_recipients(recipients)
    
    def update_recipient(self, email: str, **kwargs) -> bool:
        """Update a recipient."""
        recipients = self.load_recipients()
        for recipient in recipients:
            if recipient.email.lower() == email.lower():
                for key, value in kwargs.items():
                    if hasattr(recipient, key):
                        setattr(recipient, key, value)
                return self.save_recipients(recipients)
        return False

class TemplateManager:
    """Email template management."""
    
    def __init__(self, templates_file: str = "templates.json"):
        self.templates_file = Path(templates_file)
        self.default_templates = self._create_default_templates()
    
    def _create_default_templates(self) -> List[EmailTemplate]:
        """Create default email templates."""
        return [
            EmailTemplate(
                name="Stage PFE - HTML",
                subject="Candidature pour un stage PFE – Développement web / IA / Data",
                html_content=self._get_html_template(),
                text_content=self._get_text_template(),
                is_default=True
            )
        ]
    
    def _get_html_template(self) -> str:
        """Get HTML email template."""
        return """
        <!DOCTYPE html>
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
        </html>
        """
    
    def _get_text_template(self) -> str:
        """Get text email template."""
        return """
Bonjour {name},

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
Cette candidature est envoyée dans le cadre de ma recherche de stage PFE
        """.strip()
    
    def load_templates(self) -> List[EmailTemplate]:
        """Load templates from file."""
        try:
            if self.templates_file.exists():
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [EmailTemplate(**item) for item in data]
        except Exception as e:
            logger.warning(f"Could not load templates: {e}")
        
        return self.default_templates
    
    def save_templates(self, templates: List[EmailTemplate]) -> bool:
        """Save templates to file."""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(t) for t in templates], f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Could not save templates: {e}")
            return False

class EmailSender:
    """Robust email sending with multiple providers."""
    
    def __init__(self, config: EmailConfig):
        self.config = config
        self.server = None
        self.provider = EmailProviders.get_provider(config.provider)
    
    def validate_credentials(self) -> Tuple[bool, str]:
        """Validate email credentials."""
        if not self.config.email:
            return False, "Email address is required"
        
        if not self.config.password:
            return False, "Password is required"
        
        if '@' not in self.config.email:
            return False, "Invalid email format"
        
        if self.config.provider == "gmail" and len(self.config.password) != 16:
            return False, "Gmail App Password must be 16 characters"
        
        return True, "Credentials are valid"
    
    def connect_smtp(self) -> bool:
        """Connect to SMTP server."""
        try:
            # Validate credentials
            is_valid, error_msg = self.validate_credentials()
            if not is_valid:
                st.error(f"❌ {error_msg}")
                return False
            
            # Show connection details
            st.info(f"🔗 Connecting to {self.config.smtp_server}:{self.config.smtp_port}")
            st.info(f"📧 Using email: {self.config.email}")
            st.info(f"🔑 Provider: {self.provider.name}")
            
            # Create SMTP connection
            if self.provider.use_ssl:
                self.server = smtplib.SMTP_SSL(self.config.smtp_server, self.config.smtp_port, timeout=30)
            else:
                self.server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port, timeout=30)
                if self.provider.use_tls:
                    self.server.starttls()
            
            # Authenticate
            self.server.login(self.config.email, self.config.password)
            st.success("✅ Authentication successful!")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            st.error(f"❌ Authentication failed: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")
            return False
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   is_html: bool = True, attachment_path: Optional[str] = None) -> bool:
        """Send a single email."""
        try:
            if not self.server:
                st.error("❌ Not connected to SMTP server")
                return False
            
            # Create message
            msg = MIMEMultipart('mixed')
            msg['From'] = self.config.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            if is_html:
                msg.attach(MIMEText(body, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(attachment_path)}'
                    )
                    msg.attach(part)
            
            # Send email
            self.server.send_message(msg)
            return True
            
        except Exception as e:
            st.error(f"❌ Failed to send email to {to_email}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from SMTP server."""
        if self.server:
            try:
                self.server.quit()
            except:
                pass
            self.server = None

class EmailAutomationApp:
    """Main application class."""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.recipient_manager = RecipientManager()
        self.template_manager = TemplateManager()
        self.config = self.config_manager.load_config()
        self.recipients = self.recipient_manager.load_recipients()
        self.templates = self.template_manager.load_templates()
    
    def render_header(self):
        """Render application header."""
        st.markdown('<h1 class="main-header">📧 Email Automation Pro</h1>', unsafe_allow_html=True)
        st.markdown("---")
    
    def render_sidebar(self):
        """Render sidebar with statistics."""
        with st.sidebar:
            st.markdown("## 📊 Statistics")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Recipients", len(self.recipients))
            with col2:
                st.metric("Templates", len(self.templates))
            
            st.markdown("---")
            
            st.markdown("## ⚙️ Quick Actions")
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
            
            if st.button("📊 View Statistics", use_container_width=True):
                st.session_state.current_tab = "Statistics"
                st.rerun()
    
    def render_configuration_tab(self):
        """Render configuration tab."""
        st.markdown('<h2 class="section-header">⚙️ Configuration</h2>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="config-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔐 Email Settings")
                
                # Provider selection
                provider_options = list(EmailProviders.get_all_providers().keys())
                selected_provider = st.selectbox(
                    "Email Provider",
                    options=provider_options,
                    index=provider_options.index(self.config.provider) if self.config.provider in provider_options else 0,
                    help="Select your email provider"
                )
                
                # Update provider settings
                if selected_provider != self.config.provider:
                    provider = EmailProviders.get_provider(selected_provider)
                    self.config.provider = selected_provider
                    self.config.smtp_server = provider.smtp_server
                    self.config.smtp_port = provider.smtp_port
                
                email = st.text_input(
                    "Email Address",
                    value=self.config.email,
                    placeholder="your.email@gmail.com",
                    help="Your email address"
                )
                
                password = st.text_input(
                    "Password / App Password",
                    value=self.config.password,
                    type="password",
                    placeholder="Your password or app password",
                    help="Use App Password for Gmail (16 characters)"
                )
            
            with col2:
                st.subheader("📡 SMTP Settings")
                
                smtp_server = st.text_input(
                    "SMTP Server",
                    value=self.config.smtp_server,
                    help="SMTP server address"
                )
                
                smtp_port = st.number_input(
                    "SMTP Port",
                    value=self.config.smtp_port,
                    min_value=1,
                    max_value=65535,
                    help="SMTP server port"
                )
                
                st.subheader("⏱️ Timing Settings")
                
                col3, col4 = st.columns(2)
                with col3:
                    min_delay = st.slider(
                        "Min Delay (s)",
                        min_value=10,
                        max_value=120,
                        value=self.config.min_delay,
                        help="Minimum delay between emails"
                    )
                
                with col4:
                    max_delay = st.slider(
                        "Max Delay (s)",
                        min_value=30,
                        max_value=300,
                        value=self.config.max_delay,
                        help="Maximum delay between emails"
                    )
                
                max_emails = st.slider(
                    "Max Emails/Day",
                    min_value=5,
                    max_value=100,
                    value=self.config.max_emails_per_day,
                    help="Maximum emails per day"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Test connection
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("🔍 Test Connection", type="primary", use_container_width=True):
                test_config = EmailConfig(
                    email=email,
                    password=password,
                    provider=selected_provider,
                    smtp_server=smtp_server,
                    smtp_port=smtp_port,
                    min_delay=min_delay,
                    max_delay=max_delay,
                    max_emails_per_day=max_emails,
                    subjects=self.config.subjects,
                    greetings=self.config.greetings
                )
                
                sender = EmailSender(test_config)
                with st.spinner("Testing connection..."):
                    if sender.connect_smtp():
                        st.success("✅ Connection successful!")
                        sender.disconnect()
                    else:
                        st.error("❌ Connection failed!")
        
        # Save configuration
        if st.button("💾 Save Configuration", use_container_width=True):
            new_config = EmailConfig(
                email=email,
                password=password,
                provider=selected_provider,
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                min_delay=min_delay,
                max_delay=max_delay,
                max_emails_per_day=max_emails,
                subjects=self.config.subjects,
                greetings=self.config.greetings
            )
            
            if self.config_manager.save_config(new_config):
                st.success("✅ Configuration saved successfully!")
                self.config = new_config
                st.rerun()
            else:
                st.error("❌ Failed to save configuration!")
    
    def render_recipients_tab(self):
        """Render recipients management tab."""
        st.markdown('<h2 class="section-header">👥 Recipients Management</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Add New Recipient")
            
            with st.form("add_recipient_form"):
                new_email = st.text_input("Email Address", placeholder="recipient@company.com")
                new_name = st.text_input("Name (optional)", placeholder="John Doe")
                new_company = st.text_input("Company (optional)", placeholder="Tech Company")
                new_position = st.text_input("Position (optional)", placeholder="HR Manager")
                new_notes = st.text_area("Notes (optional)", placeholder="Additional notes...")
                
                if st.form_submit_button("➕ Add Recipient", use_container_width=True):
                    if new_email and '@' in new_email:
                        if self.recipient_manager.add_recipient(
                            new_email, new_name, new_company, new_position, new_notes
                        ):
                            st.success(f"✅ Added {new_email}")
                            self.recipients = self.recipient_manager.load_recipients()
                            st.rerun()
                        else:
                            st.error("❌ Email already exists or failed to add")
                    else:
                        st.error("❌ Please enter a valid email address")
        
        with col2:
            st.subheader("Bulk Import")
            
            csv_file = st.file_uploader(
                "Upload CSV",
                type=['csv'],
                help="CSV with columns: email, name, company, position"
            )
            
            if csv_file:
                try:
                    df = pd.read_csv(csv_file)
                    if 'email' in df.columns:
                        added_count = 0
                        for _, row in df.iterrows():
                            if pd.notna(row['email']):
                                if self.recipient_manager.add_recipient(
                                    str(row['email']),
                                    str(row.get('name', '')),
                                    str(row.get('company', '')),
                                    str(row.get('position', '')),
                                    str(row.get('notes', ''))
                                ):
                                    added_count += 1
                        st.success(f"✅ Added {added_count} recipients")
                        self.recipients = self.recipient_manager.load_recipients()
                        st.rerun()
                    else:
                        st.error("❌ CSV must have 'email' column")
                except Exception as e:
                    st.error(f"❌ Error reading CSV: {e}")
        
        # Display recipients
        st.subheader("📋 Current Recipients")
        
        if self.recipients:
            # Create DataFrame for display
            df_data = []
            for i, recipient in enumerate(self.recipients):
                df_data.append({
                    'Email': recipient.email,
                    'Name': recipient.name or '-',
                    'Company': recipient.company or '-',
                    'Position': recipient.position or '-',
                    'Status': recipient.status,
                    'Actions': f"Edit_{i}"
                })
            
            df = pd.DataFrame(df_data)
            
            # Display with actions
            for i, recipient in enumerate(self.recipients):
                with st.expander(f"📧 {recipient.email} - {recipient.name or 'No name'}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Company:** {recipient.company or 'Not specified'}")
                        st.write(f"**Position:** {recipient.position or 'Not specified'}")
                        if recipient.notes:
                            st.write(f"**Notes:** {recipient.notes}")
                    
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{i}"):
                            st.session_state[f"edit_recipient_{i}"] = True
                    
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_{i}"):
                            if self.recipient_manager.remove_recipient(recipient.email):
                                st.success(f"✅ Removed {recipient.email}")
                                self.recipients = self.recipient_manager.load_recipients()
                                st.rerun()
                            else:
                                st.error("❌ Failed to remove recipient")
        else:
            st.info("📭 No recipients added yet")
    
    def render_send_emails_tab(self):
        """Render email sending tab."""
        st.markdown('<h2 class="section-header">📧 Send Emails</h2>', unsafe_allow_html=True)
        
        if not self.recipients:
            st.warning("⚠️ No recipients found. Please add recipients first.")
            return
        
        if not self.config.email or not self.config.password:
            st.warning("⚠️ Please configure your email settings first.")
            return
        
        # Email settings
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Email Settings")
            
            # Template selection
            template_options = [f"{t.name} ({'HTML' if t.html_content else 'Text'})" for t in self.templates]
            selected_template_idx = st.selectbox(
                "Email Template",
                options=range(len(template_options)),
                format_func=lambda x: template_options[x],
                help="Choose email template"
            )
            
            selected_template = self.templates[selected_template_idx]
            
            # Subject selection
            subject = st.selectbox(
                "Subject Line",
                options=self.config.subjects,
                help="Choose email subject"
            )
            
            # Email type
            email_type = st.radio(
                "Email Format",
                options=["HTML", "Text"],
                help="Choose email format"
            )
        
        with col2:
            st.subheader("📊 Sending Settings")
            
            num_emails = st.slider(
                "Number of Emails",
                min_value=1,
                max_value=min(len(self.recipients), self.config.max_emails_per_day),
                value=min(5, len(self.recipients)),
                help="Number of emails to send"
            )
            
            attachment_path = st.text_input(
                "Attachment Path (optional)",
                placeholder="path/to/cv.pdf",
                help="Path to CV or other attachment"
            )
            
            if attachment_path and not os.path.exists(attachment_path):
                st.warning("⚠️ Attachment file not found")
        
        # Preview
        if st.button("👁️ Preview Email", use_container_width=True):
            sample_recipient = self.recipients[0]
            if email_type == "HTML":
                preview_content = selected_template.html_content.format(
                    name=sample_recipient.name or "John Doe",
                    company=sample_recipient.company or "Tech Company",
                    email=self.config.email
                )
                st.markdown("**Email Preview:**")
                st.components.v1.html(preview_content, height=400, scrolling=True)
            else:
                preview_content = selected_template.text_content.format(
                    name=sample_recipient.name or "John Doe",
                    company=sample_recipient.company or "Tech Company",
                    email=self.config.email
                )
                st.markdown("**Email Preview:**")
                st.text(preview_content)
        
        # Send emails
        if st.button("🚀 Start Sending", type="primary", use_container_width=True):
            # Initialize email sender
            sender = EmailSender(self.config)
            
            # Connect to SMTP
            with st.spinner("Connecting to email server..."):
                if not sender.connect_smtp():
                    st.error("❌ Failed to connect. Please check your configuration.")
                    return
            
            st.success("✅ Connected successfully!")
            
            # Send emails
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            sent_count = 0
            failed_count = 0
            
            for i, recipient in enumerate(self.recipients[:num_emails]):
                try:
                    # Update progress
                    progress = (i + 1) / num_emails
                    progress_bar.progress(progress)
                    status_text.text(f"Sending email {i + 1}/{num_emails} to {recipient.email}")
                    
                    # Create email content
                    if email_type == "HTML":
                        content = selected_template.html_content.format(
                            name=recipient.name or "",
                            company=recipient.company or "",
                            email=self.config.email
                        )
                    else:
                        content = selected_template.text_content.format(
                            name=recipient.name or "",
                            company=recipient.company or "",
                            email=self.config.email
                        )
                    
                    # Send email
                    if sender.send_email(
                        recipient.email,
                        subject,
                        content,
                        is_html=(email_type == "HTML"),
                        attachment_path=attachment_path if attachment_path and os.path.exists(attachment_path) else None
                    ):
                        sent_count += 1
                        st.success(f"✅ Sent to {recipient.email}")
                        
                        # Update recipient status
                        self.recipient_manager.update_recipient(
                            recipient.email,
                            last_contacted=datetime.now().isoformat()
                        )
                    else:
                        failed_count += 1
                        st.error(f"❌ Failed to send to {recipient.email}")
                    
                    # Random delay between emails
                    if i < num_emails - 1:
                        delay = random.randint(self.config.min_delay, self.config.max_delay)
                        time.sleep(delay)
                
                except Exception as e:
                    failed_count += 1
                    st.error(f"❌ Error sending to {recipient.email}: {e}")
            
            # Disconnect
            sender.disconnect()
            
            # Final status
            progress_bar.progress(1.0)
            status_text.text("✅ Email sending completed!")
            
            st.success(f"📊 Results: {sent_count} sent, {failed_count} failed")
    
    def render_statistics_tab(self):
        """Render statistics tab."""
        st.markdown('<h2 class="section-header">📊 Statistics</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Recipients", len(self.recipients))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            companies = len(set(r.company for r in self.recipients if r.company))
            st.metric("Unique Companies", companies)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Email Templates", len(self.templates))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("App Status", "🟢 Active")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed statistics
        if self.recipients:
            st.subheader("📈 Recipients Overview")
            
            # Create summary DataFrame
            df_data = []
            for recipient in self.recipients:
                df_data.append({
                    'Email': recipient.email,
                    'Name': recipient.name or '-',
                    'Company': recipient.company or '-',
                    'Position': recipient.position or '-',
                    'Status': recipient.status,
                    'Added': recipient.added_date[:10] if recipient.added_date else '-',
                    'Last Contacted': recipient.last_contacted[:10] if recipient.last_contacted else 'Never'
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Company distribution
            if any(r.company for r in self.recipients):
                st.subheader("🏢 Company Distribution")
                company_counts = pd.Series([r.company for r in self.recipients if r.company]).value_counts()
                st.bar_chart(company_counts)
    
    def run(self):
        """Run the application."""
        self.render_header()
        self.render_sidebar()
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "⚙️ Configuration", 
            "👥 Recipients", 
            "📧 Send Emails", 
            "📊 Statistics"
        ])
        
        with tab1:
            self.render_configuration_tab()
        
        with tab2:
            self.render_recipients_tab()
        
        with tab3:
            self.render_send_emails_tab()
        
        with tab4:
            self.render_statistics_tab()

def main():
    """Main application entry point."""
    app = EmailAutomationApp()
    app.run()

if __name__ == "__main__":
    main()
