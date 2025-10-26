"""
Email Automation App - Clean Rebuild
A modern, robust email automation system with Gmail integration.
"""

import streamlit as st
import smtplib
import ssl
import csv
import json
import os
import time
import random
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional, Tuple
import pandas as pd

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
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .config-section {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class EmailConfig:
    """Email configuration management."""
    
    def __init__(self):
        self.config_file = "email_config.json"
        self.default_config = {
            "email": "",
            "app_password": "",
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
            "greetings": [
                "Bonjour",
                "Salut",
                "Bonjour"
            ]
        }
    
    def load_config(self) -> Dict:
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**self.default_config, **config}
        except Exception as e:
            st.warning(f"⚠️ Could not load config: {e}")
        return self.default_config.copy()
    
    def save_config(self, config: Dict) -> bool:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"❌ Could not save config: {e}")
            return False

class EmailSender:
    """Robust email sending with multiple authentication methods."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.server = None
    
    def validate_credentials(self) -> Tuple[bool, str]:
        """Validate email credentials."""
        email = self.config.get('email', '').strip()
        password = self.config.get('app_password', '').strip()
        
        if not email:
            return False, "Email address is required"
        
        if not password:
            return False, "App password is required"
        
        if '@' not in email:
            return False, "Invalid email format"
        
        if len(password) != 16:
            return False, "App password must be 16 characters"
        
        return True, "Credentials are valid"
    
    def connect_smtp(self) -> bool:
        """Connect to SMTP server with multiple retry methods."""
        try:
            # Validate credentials first
            is_valid, error_msg = self.validate_credentials()
            if not is_valid:
                st.error(f"❌ {error_msg}")
                return False
            
            email = self.config['email']
            password = self.config['app_password']
            server = self.config['smtp_server']
            port = self.config['smtp_port']
            
            # Show connection details
            st.info(f"🔗 Connecting to {server}:{port}")
            st.info(f"📧 Using email: {email}")
            st.info(f"🔑 App password: {'*' * 16} (length: 16)")
            
            # Method 1: Standard TLS connection
            try:
                st.info("🔒 Starting TLS encryption...")
                self.server = smtplib.SMTP(server, port, timeout=30)
                self.server.starttls()
                
                st.info("🔐 Attempting authentication...")
                self.server.login(email, password)
                st.success("✅ Authentication successful!")
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                st.warning("⚠️ Standard authentication failed, trying alternative method...")
                
                # Method 2: Alternative connection
                try:
                    self.server.quit()
                    self.server = smtplib.SMTP(server, port, timeout=30)
                    self.server.starttls()
                    self.server.login(email, password)
                    st.success("✅ Alternative authentication successful!")
                    return True
                    
                except Exception as e2:
                    st.error(f"❌ Alternative authentication failed: {e2}")
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
            msg['From'] = self.config['email']
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

class EmailTemplate:
    """Email template management."""
    
    @staticmethod
    def create_html_template(name: str, company: str, email: str) -> str:
        """Create professional HTML email template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #1f77b4; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ background-color: #333; color: white; padding: 15px; text-align: center; font-size: 12px; }}
                .signature {{ margin-top: 20px; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Candidature pour Stage PFE</h2>
                </div>
                <div class="content">
                    <p>Bonjour {name},</p>
                    
                    <p>Je me permets de vous contacter pour vous faire part de mon intérêt pour un stage de fin d'études (PFE) au sein de votre entreprise {company}.</p>
                    
                    <p>Actuellement étudiant en dernière année, je suis passionné par le développement web, l'intelligence artificielle et les technologies numériques. Mon parcours académique et mes projets personnels m'ont permis d'acquérir des compétences solides dans ces domaines.</p>
                    
                    <p>Je serais ravi de pouvoir échanger avec vous sur les opportunités de stage disponibles et de vous présenter mon profil plus en détail.</p>
                    
                    <p>Je vous remercie sincèrement pour votre temps et votre considération.</p>
                    
                    <div class="signature">
                        <p>Cordialement,<br>
                        Othmane Chaikhi<br>
                        Email: {email}<br>
                        Téléphone: +212 631-889579</p>
                    </div>
                </div>
                <div class="footer">
                    <p>Cette candidature est envoyée dans le cadre de ma recherche de stage PFE</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def create_text_template(name: str, company: str, email: str) -> str:
        """Create plain text email template."""
        return f"""
Bonjour {name},

Je me permets de vous contacter pour vous faire part de mon intérêt pour un stage de fin d'études (PFE) au sein de votre entreprise {company}.

Actuellement étudiant en dernière année, je suis passionné par le développement web, l'intelligence artificielle et les technologies numériques. Mon parcours académique et mes projets personnels m'ont permis d'acquérir des compétences solides dans ces domaines.

Je serais ravi de pouvoir échanger avec vous sur les opportunités de stage disponibles et de vous présenter mon profil plus en détail.

Je vous remercie sincèrement pour votre temps et votre considération.

Cordialement,
Othmane Chaikhi
Email: {email}
Téléphone: +212 631-889579

---
Cette candidature est envoyée dans le cadre de ma recherche de stage PFE
        """.strip()

class RecipientManager:
    """Manage email recipients."""
    
    def __init__(self):
        self.recipients_file = "recipients.json"
    
    def load_recipients(self) -> List[Dict]:
        """Load recipients from file."""
        try:
            if os.path.exists(self.recipients_file):
                with open(self.recipients_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            st.warning(f"⚠️ Could not load recipients: {e}")
        return []
    
    def save_recipients(self, recipients: List[Dict]) -> bool:
        """Save recipients to file."""
        try:
            with open(self.recipients_file, 'w', encoding='utf-8') as f:
                json.dump(recipients, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"❌ Could not save recipients: {e}")
            return False
    
    def add_recipient(self, email: str, name: str = "", company: str = "") -> bool:
        """Add a new recipient."""
        recipients = self.load_recipients()
        
        # Check if email already exists
        if any(r.get('email', '').lower() == email.lower() for r in recipients):
            st.warning(f"⚠️ Email {email} already exists")
            return False
        
        recipients.append({
            'email': email.lower(),
            'name': name,
            'company': company,
            'added_date': datetime.now().isoformat()
        })
        
        return self.save_recipients(recipients)
    
    def remove_recipient(self, email: str) -> bool:
        """Remove a recipient."""
        recipients = self.load_recipients()
        recipients = [r for r in recipients if r.get('email', '').lower() != email.lower()]
        return self.save_recipients(recipients)

def main():
    """Main application."""
    st.markdown('<h1 class="main-header">📧 Email Automation Pro</h1>', unsafe_allow_html=True)
    
    # Initialize managers
    config_manager = EmailConfig()
    recipient_manager = RecipientManager()
    
    # Load configuration
    config = config_manager.load_config()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["⚙️ Configuration", "👥 Recipients", "📧 Send Emails", "📊 Statistics"])
    
    with tab1:
        st.header("⚙️ Email Configuration")
        
        with st.container():
            st.markdown('<div class="config-section">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔐 Gmail Settings")
                email = st.text_input(
                    "Gmail Address",
                    value=config.get('email', ''),
                    placeholder="your.email@gmail.com",
                    help="Your Gmail address"
                )
                
                app_password = st.text_input(
                    "App Password",
                    value=config.get('app_password', ''),
                    type="password",
                    placeholder="16-character app password",
                    help="Gmail App Password (not your regular password)"
                )
            
            with col2:
                st.subheader("📡 SMTP Settings")
                smtp_server = st.text_input(
                    "SMTP Server",
                    value=config.get('smtp_server', 'smtp.gmail.com'),
                    help="SMTP server address"
                )
                
                smtp_port = st.number_input(
                    "SMTP Port",
                    value=config.get('smtp_port', 587),
                    min_value=1,
                    max_value=65535,
                    help="SMTP server port"
                )
            
            st.subheader("⏱️ Timing Settings")
            col3, col4 = st.columns(2)
            
            with col3:
                min_delay = st.slider(
                    "Minimum Delay (seconds)",
                    min_value=10,
                    max_value=120,
                    value=config.get('min_delay', 30),
                    help="Minimum time between emails"
                )
            
            with col4:
                max_delay = st.slider(
                    "Maximum Delay (seconds)",
                    min_value=30,
                    max_value=300,
                    value=config.get('max_delay', 60),
                    help="Maximum time between emails"
                )
            
            max_emails = st.slider(
                "Max Emails Per Day",
                min_value=5,
                max_value=100,
                value=config.get('max_emails_per_day', 50),
                help="Maximum emails to send in one session"
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Test connection button
        if st.button("🔍 Test Gmail Connection", type="primary"):
            test_config = {
                'email': email,
                'app_password': app_password,
                'smtp_server': smtp_server,
                'smtp_port': smtp_port
            }
            
            sender = EmailSender(test_config)
            with st.spinner("Testing connection..."):
                if sender.connect_smtp():
                    st.success("✅ Gmail connection successful!")
                    sender.disconnect()
                else:
                    st.error("❌ Gmail connection failed!")
        
        # Save configuration
        if st.button("💾 Save Configuration"):
            new_config = {
                'email': email,
                'app_password': app_password,
                'smtp_server': smtp_server,
                'smtp_port': smtp_port,
                'min_delay': min_delay,
                'max_delay': max_delay,
                'max_emails_per_day': max_emails,
                'subjects': config.get('subjects', []),
                'greetings': config.get('greetings', [])
            }
            
            if config_manager.save_config(new_config):
                st.success("✅ Configuration saved successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to save configuration!")
    
    with tab2:
        st.header("👥 Manage Recipients")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Add New Recipient")
            
            with st.form("add_recipient_form"):
                new_email = st.text_input("Email Address", placeholder="recipient@company.com")
                new_name = st.text_input("Name (optional)", placeholder="John Doe")
                new_company = st.text_input("Company (optional)", placeholder="Tech Company")
                
                if st.form_submit_button("➕ Add Recipient"):
                    if new_email and '@' in new_email:
                        if recipient_manager.add_recipient(new_email, new_name, new_company):
                            st.success(f"✅ Added {new_email}")
                            st.rerun()
                        else:
                            st.error("❌ Failed to add recipient")
                    else:
                        st.error("❌ Please enter a valid email address")
        
        with col2:
            st.subheader("Bulk Import")
            
            csv_file = st.file_uploader(
                "Upload CSV",
                type=['csv'],
                help="CSV with columns: email, name, company"
            )
            
            if csv_file:
                try:
                    df = pd.read_csv(csv_file)
                    if 'email' in df.columns:
                        added_count = 0
                        for _, row in df.iterrows():
                            if pd.notna(row['email']):
                                if recipient_manager.add_recipient(
                                    str(row['email']),
                                    str(row.get('name', '')),
                                    str(row.get('company', ''))
                                ):
                                    added_count += 1
                        st.success(f"✅ Added {added_count} recipients")
                        st.rerun()
                    else:
                        st.error("❌ CSV must have 'email' column")
                except Exception as e:
                    st.error(f"❌ Error reading CSV: {e}")
        
        # Display recipients
        st.subheader("📋 Current Recipients")
        recipients = recipient_manager.load_recipients()
        
        if recipients:
            df = pd.DataFrame(recipients)
            df['Actions'] = df['email'].apply(lambda x: f"🗑️ {x}")
            
            # Display with delete buttons
            for i, recipient in enumerate(recipients):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(recipient['email'])
                with col2:
                    st.write(recipient.get('name', '-'))
                with col3:
                    st.write(recipient.get('company', '-'))
                with col4:
                    if st.button("🗑️", key=f"delete_{i}"):
                        if recipient_manager.remove_recipient(recipient['email']):
                            st.success(f"✅ Removed {recipient['email']}")
                            st.rerun()
                        else:
                            st.error("❌ Failed to remove recipient")
        else:
            st.info("📭 No recipients added yet")
    
    with tab3:
        st.header("📧 Send Emails")
        
        # Load current config
        current_config = config_manager.load_config()
        recipients = recipient_manager.load_recipients()
        
        if not recipients:
            st.warning("⚠️ No recipients found. Please add recipients first.")
            return
        
        if not current_config.get('email') or not current_config.get('app_password'):
            st.warning("⚠️ Please configure your Gmail settings first.")
            return
        
        # Email settings
        st.subheader("📝 Email Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox(
                "Subject Line",
                options=current_config.get('subjects', []),
                help="Choose email subject"
            )
        
        with col2:
            email_type = st.radio(
                "Email Type",
                options=["HTML", "Text"],
                help="Choose email format"
            )
        
        # Preview
        if st.button("👁️ Preview Email"):
            sample_recipient = recipients[0]
            if email_type == "HTML":
                preview_content = EmailTemplate.create_html_template(
                    sample_recipient.get('name', 'John Doe'),
                    sample_recipient.get('company', 'Tech Company'),
                    current_config['email']
                )
                st.markdown("**Email Preview:**")
                st.components.v1.html(preview_content, height=400, scrolling=True)
            else:
                preview_content = EmailTemplate.create_text_template(
                    sample_recipient.get('name', 'John Doe'),
                    sample_recipient.get('company', 'Tech Company'),
                    current_config['email']
                )
                st.markdown("**Email Preview:**")
                st.text(preview_content)
        
        # Send emails
        st.subheader("🚀 Send Emails")
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_emails = st.slider(
                "Number of Emails to Send",
                min_value=1,
                max_value=min(len(recipients), current_config.get('max_emails_per_day', 50)),
                value=min(5, len(recipients)),
                help="Number of emails to send in this session"
            )
        
        with col2:
            attachment_path = st.text_input(
                "Attachment Path (optional)",
                placeholder="path/to/cv.pdf",
                help="Path to CV or other attachment"
            )
        
        if st.button("🚀 Start Sending", type="primary"):
            # Initialize email sender
            sender = EmailSender(current_config)
            
            # Connect to SMTP
            with st.spinner("Connecting to Gmail..."):
                if not sender.connect_smtp():
                    st.error("❌ Failed to connect to Gmail. Please check your configuration.")
                    return
            
            st.success("✅ Connected to Gmail successfully!")
            
            # Send emails
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            sent_count = 0
            failed_count = 0
            
            for i, recipient in enumerate(recipients[:num_emails]):
                try:
                    # Update progress
                    progress = (i + 1) / num_emails
                    progress_bar.progress(progress)
                    status_text.text(f"Sending email {i + 1}/{num_emails} to {recipient['email']}")
                    
                    # Create email content
                    if email_type == "HTML":
                        content = EmailTemplate.create_html_template(
                            recipient.get('name', ''),
                            recipient.get('company', ''),
                            current_config['email']
                        )
                    else:
                        content = EmailTemplate.create_text_template(
                            recipient.get('name', ''),
                            recipient.get('company', ''),
                            current_config['email']
                        )
                    
                    # Send email
                    if sender.send_email(
                        recipient['email'],
                        subject,
                        content,
                        is_html=(email_type == "HTML"),
                        attachment_path=attachment_path if attachment_path and os.path.exists(attachment_path) else None
                    ):
                        sent_count += 1
                        st.success(f"✅ Sent to {recipient['email']}")
                    else:
                        failed_count += 1
                        st.error(f"❌ Failed to send to {recipient['email']}")
                    
                    # Random delay between emails
                    if i < num_emails - 1:  # Don't delay after last email
                        delay = random.randint(
                            current_config.get('min_delay', 30),
                            current_config.get('max_delay', 60)
                        )
                        time.sleep(delay)
                
                except Exception as e:
                    failed_count += 1
                    st.error(f"❌ Error sending to {recipient['email']}: {e}")
            
            # Disconnect
            sender.disconnect()
            
            # Final status
            progress_bar.progress(1.0)
            status_text.text("✅ Email sending completed!")
            
            st.success(f"📊 Results: {sent_count} sent, {failed_count} failed")
    
    with tab4:
        st.header("📊 Statistics")
        
        recipients = recipient_manager.load_recipients()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Recipients", len(recipients))
        
        with col2:
            companies = len(set(r.get('company', '') for r in recipients if r.get('company')))
            st.metric("Unique Companies", companies)
        
        with col3:
            st.metric("App Status", "🟢 Active")
        
        if recipients:
            st.subheader("📈 Recipients Overview")
            df = pd.DataFrame(recipients)
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
