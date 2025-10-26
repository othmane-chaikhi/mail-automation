"""
Simple Email Automation App
A simplified version that's guaranteed to work.
"""

import streamlit as st
import smtplib
import json
import os
import time
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Page configuration
st.set_page_config(
    page_title="Email Automation",
    page_icon="📧",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        font-size: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_config():
    """Load configuration from file."""
    try:
        if os.path.exists("config.json"):
            with open("config.json", 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading config: {e}")
    
    return {
        "email": "",
        "password": "",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "min_delay": 30,
        "max_delay": 60,
        "max_emails_per_day": 50
    }

def save_config(config):
    """Save configuration to file."""
    try:
        with open("config.json", 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving config: {e}")
        return False

def load_recipients():
    """Load recipients from file."""
    try:
        if os.path.exists("recipients.json"):
            with open("recipients.json", 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading recipients: {e}")
    
    return []

def save_recipients(recipients):
    """Save recipients to file."""
    try:
        with open("recipients.json", 'w') as f:
            json.dump(recipients, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving recipients: {e}")
        return False

def test_email_connection(email, password, smtp_server, smtp_port):
    """Test email connection."""
    try:
        st.info(f"🔗 Connecting to {smtp_server}:{smtp_port}")
        st.info(f"📧 Using email: {email}")
        
        # Create SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        server.starttls()
        server.login(email, password)
        server.quit()
        
        return True, "Connection successful!"
    except Exception as e:
        return False, f"Connection failed: {e}"

def send_email(email, password, smtp_server, smtp_port, to_email, subject, body, is_html=True):
    """Send a single email."""
    try:
        # Create SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        server.starttls()
        server.login(email, password)
        
        # Create message
        msg = MIMEMultipart('mixed')
        msg['From'] = email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body
        if is_html:
            msg.attach(MIMEText(body, 'html', 'utf-8'))
        else:
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"Failed to send email to {to_email}: {e}")
        return False

def create_html_template(name, company, email):
    """Create HTML email template."""
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
                
                <p>Actuellement étudiant en dernière année, je suis passionné par le développement web, l'intelligence artificielle et les technologies numériques.</p>
                
                <p>Je serais ravi de pouvoir échanger avec vous sur les opportunités de stage disponibles.</p>
                
                <p>Je vous remercie sincèrement pour votre temps et votre considération.</p>
                
                <p><strong>Cordialement,<br>
                Othmane Chaikhi<br>
                Email: {email}<br>
                Téléphone: +212 631-889579</strong></p>
            </div>
            <div class="footer">
                <p>Cette candidature est envoyée dans le cadre de ma recherche de stage PFE</p>
            </div>
        </div>
    </body>
    </html>
    """

def main():
    """Main application."""
    st.markdown('<h1 class="main-header">📧 Email Automation</h1>', unsafe_allow_html=True)
    
    # Load data
    config = load_config()
    recipients = load_recipients()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["⚙️ Configuration", "👥 Recipients", "📧 Send Emails"])
    
    with tab1:
        st.header("⚙️ Email Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input("Gmail Address", value=config.get('email', ''), placeholder="your.email@gmail.com")
            password = st.text_input("App Password", value=config.get('password', ''), type="password", placeholder="16-character app password")
        
        with col2:
            smtp_server = st.text_input("SMTP Server", value=config.get('smtp_server', 'smtp.gmail.com'))
            smtp_port = st.number_input("SMTP Port", value=config.get('smtp_port', 587), min_value=1, max_value=65535)
        
        # Test connection
        if st.button("🔍 Test Connection", type="primary"):
            if email and password:
                success, message = test_email_connection(email, password, smtp_server, smtp_port)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("❌ Please enter email and password")
        
        # Save configuration
        if st.button("💾 Save Configuration"):
            new_config = {
                "email": email,
                "password": password,
                "smtp_server": smtp_server,
                "smtp_port": smtp_port,
                "min_delay": config.get('min_delay', 30),
                "max_delay": config.get('max_delay', 60),
                "max_emails_per_day": config.get('max_emails_per_day', 50)
            }
            
            if save_config(new_config):
                st.success("✅ Configuration saved!")
                config = new_config
            else:
                st.error("❌ Failed to save configuration")
    
    with tab2:
        st.header("👥 Recipients Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Add Recipient")
            
            with st.form("add_recipient"):
                new_email = st.text_input("Email Address", placeholder="recipient@company.com")
                new_name = st.text_input("Name (optional)", placeholder="John Doe")
                new_company = st.text_input("Company (optional)", placeholder="Tech Company")
                
                if st.form_submit_button("➕ Add Recipient"):
                    if new_email and '@' in new_email:
                        # Check if email already exists
                        if not any(r.get('email', '').lower() == new_email.lower() for r in recipients):
                            recipients.append({
                                'email': new_email.lower(),
                                'name': new_name,
                                'company': new_company,
                                'added_date': datetime.now().isoformat()
                            })
                            
                            if save_recipients(recipients):
                                st.success(f"✅ Added {new_email}")
                                st.rerun()
                            else:
                                st.error("❌ Failed to save recipient")
                        else:
                            st.error("❌ Email already exists")
                    else:
                        st.error("❌ Please enter a valid email address")
        
        with col2:
            st.subheader("Current Recipients")
            
            if recipients:
                for i, recipient in enumerate(recipients):
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.write(f"📧 {recipient['email']}")
                        if recipient.get('name'):
                            st.write(f"👤 {recipient['name']}")
                        if recipient.get('company'):
                            st.write(f"🏢 {recipient['company']}")
                    
                    with col_b:
                        if st.button("🗑️", key=f"delete_{i}"):
                            recipients.pop(i)
                            save_recipients(recipients)
                            st.rerun()
            else:
                st.info("No recipients added yet")
    
    with tab3:
        st.header("📧 Send Emails")
        
        if not recipients:
            st.warning("⚠️ No recipients found. Please add recipients first.")
            return
        
        if not config.get('email') or not config.get('password'):
            st.warning("⚠️ Please configure your email settings first.")
            return
        
        # Email settings
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox(
                "Subject Line",
                options=[
                    "Candidature pour un stage PFE – Développement web / IA / Data",
                    "Candidature stage PFE - Technologies numériques",
                    "Candidature spontanée - Stage PFE Développement / IA",
                    "Candidature pour un stage PFE - Intelligence Artificielle"
                ]
            )
            
            email_type = st.radio("Email Format", ["HTML", "Text"])
        
        with col2:
            num_emails = st.slider(
                "Number of Emails",
                min_value=1,
                max_value=min(len(recipients), 10),
                value=min(3, len(recipients))
            )
        
        # Preview
        if st.button("👁️ Preview Email"):
            sample_recipient = recipients[0]
            if email_type == "HTML":
                preview_content = create_html_template(
                    sample_recipient.get('name', 'John Doe'),
                    sample_recipient.get('company', 'Tech Company'),
                    config['email']
                )
                st.components.v1.html(preview_content, height=400, scrolling=True)
            else:
                preview_content = f"""
Bonjour {sample_recipient.get('name', 'John Doe')},

Je me permets de vous contacter pour vous faire part de mon intérêt pour un stage de fin d'études (PFE) au sein de votre entreprise {sample_recipient.get('company', 'Tech Company')}.

Actuellement étudiant en dernière année, je suis passionné par le développement web, l'intelligence artificielle et les technologies numériques.

Je serais ravi de pouvoir échanger avec vous sur les opportunités de stage disponibles.

Je vous remercie sincèrement pour votre temps et votre considération.

Cordialement,
Othmane Chaikhi
Email: {config['email']}
Téléphone: +212 631-889579
                """.strip()
                st.text(preview_content)
        
        # Send emails
        if st.button("🚀 Start Sending", type="primary"):
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
                        content = create_html_template(
                            recipient.get('name', ''),
                            recipient.get('company', ''),
                            config['email']
                        )
                    else:
                        content = f"""
Bonjour {recipient.get('name', '')},

Je me permets de vous contacter pour vous faire part de mon intérêt pour un stage de fin d'études (PFE) au sein de votre entreprise {recipient.get('company', '')}.

Actuellement étudiant en dernière année, je suis passionné par le développement web, l'intelligence artificielle et les technologies numériques.

Je serais ravi de pouvoir échanger avec vous sur les opportunités de stage disponibles.

Je vous remercie sincèrement pour votre temps et votre considération.

Cordialement,
Othmane Chaikhi
Email: {config['email']}
Téléphone: +212 631-889579
                        """.strip()
                    
                    # Send email
                    if send_email(
                        config['email'],
                        config['password'],
                        config['smtp_server'],
                        config['smtp_port'],
                        recipient['email'],
                        subject,
                        content,
                        is_html=(email_type == "HTML")
                    ):
                        sent_count += 1
                        st.success(f"✅ Sent to {recipient['email']}")
                    else:
                        failed_count += 1
                        st.error(f"❌ Failed to send to {recipient['email']}")
                    
                    # Delay between emails
                    if i < num_emails - 1:
                        time.sleep(random.randint(30, 60))
                
                except Exception as e:
                    failed_count += 1
                    st.error(f"❌ Error sending to {recipient['email']}: {e}")
            
            # Final status
            progress_bar.progress(1.0)
            status_text.text("✅ Email sending completed!")
            
            st.success(f"📊 Results: {sent_count} sent, {failed_count} failed")

if __name__ == "__main__":
    main()
