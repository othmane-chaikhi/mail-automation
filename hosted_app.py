"""
Hosted Email Automation App
Optimized for hosted environments like Streamlit Cloud
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

# Page configuration
st.set_page_config(
    page_title="Email Automation Pro",
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
        font-size: 2.5rem;
        font-weight: bold;
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
</style>
""", unsafe_allow_html=True)

def load_config():
    """Load configuration from file or create default."""
    default_config = {
        "email": "",
        "password": "",
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
        ]
    }
    
    try:
        if os.path.exists("config.json"):
            with open("config.json", 'r') as f:
                config = json.load(f)
                return {**default_config, **config}
    except Exception as e:
        st.warning(f"Could not load config: {e}")
    
    return default_config

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
        st.warning(f"Could not load recipients: {e}")
    
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

def test_gmail_connection(email, password, smtp_server, smtp_port):
    """Test Gmail connection with detailed feedback."""
    try:
        st.info(f"🔗 Connecting to {smtp_server}:{smtp_port}")
        st.info(f"📧 Using email: {email}")
        st.info(f"🔑 App password: {'*' * len(password)} (length: {len(password)})")
        
        # Create SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        server.starttls()
        server.login(email, password)
        server.quit()
        
        return True, "✅ Connection successful!"
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"❌ Authentication failed: {e}"
        troubleshooting = """
        🔧 Troubleshooting Steps:
        
        1. **Generate a NEW App Password:**
           - Go to https://myaccount.google.com/security
           - Click 'App passwords' (only visible with 2FA enabled)
           - Delete the old password and create a new one
           - Copy the NEW 16-character password
        
        2. **Check 2-Factor Authentication:**
           - Ensure 2FA is enabled on your Google account
           - App passwords only work with 2FA enabled
        
        3. **Wait and Retry:**
           - New App passwords can take 5-10 minutes to activate
           - Try again after a few minutes
        """
        return False, error_msg + "\n\n" + troubleshooting
        
    except Exception as e:
        return False, f"❌ Connection failed: {e}"

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
    """Create professional HTML email template."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; background: #f8f9fa; }}
            .footer {{ background: #2c3e50; color: white; padding: 20px; text-align: center; font-size: 12px; }}
            .signature {{ margin-top: 25px; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .highlight {{ background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0; }}
            h1 {{ margin: 0; font-size: 24px; }}
            h2 {{ color: #2c3e50; margin-top: 0; }}
            .contact-info {{ background: #f1f3f4; padding: 15px; border-radius: 8px; margin-top: 20px; }}
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

def main():
    """Main application."""
    st.markdown('<h1 class="main-header">📧 Email Automation Pro</h1>', unsafe_allow_html=True)
    
    # Load data
    config = load_config()
    recipients = load_recipients()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["⚙️ Configuration", "👥 Recipients", "📧 Send Emails", "📊 Statistics"])
    
    with tab1:
        st.markdown('<h2 class="section-header">⚙️ Email Configuration</h2>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="config-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔐 Gmail Settings")
                email = st.text_input(
                    "Gmail Address",
                    value=config.get('email', ''),
                    placeholder="your.email@gmail.com",
                    help="Your Gmail address"
                )
                
                password = st.text_input(
                    "App Password",
                    value=config.get('password', ''),
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
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Test connection
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("🔍 Test Gmail Connection", type="primary", use_container_width=True):
                if email and password:
                    success, message = test_gmail_connection(email, password, smtp_server, smtp_port)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("❌ Please enter email and password")
        
        # Save configuration
        if st.button("💾 Save Configuration", use_container_width=True):
            new_config = {
                "email": email,
                "password": password,
                "smtp_server": smtp_server,
                "smtp_port": smtp_port,
                "min_delay": config.get('min_delay', 30),
                "max_delay": config.get('max_delay', 60),
                "max_emails_per_day": config.get('max_emails_per_day', 50),
                "subjects": config.get('subjects', [])
            }
            
            if save_config(new_config):
                st.success("✅ Configuration saved successfully!")
                config = new_config
                st.rerun()
            else:
                st.error("❌ Failed to save configuration!")
    
    with tab2:
        st.markdown('<h2 class="section-header">👥 Recipients Management</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Add New Recipient")
            
            with st.form("add_recipient_form"):
                new_email = st.text_input("Email Address", placeholder="recipient@company.com")
                new_name = st.text_input("Name (optional)", placeholder="John Doe")
                new_company = st.text_input("Company (optional)", placeholder="Tech Company")
                
                if st.form_submit_button("➕ Add Recipient", use_container_width=True):
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
        st.markdown('<h2 class="section-header">📧 Send Emails</h2>', unsafe_allow_html=True)
        
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
                options=config.get('subjects', []),
                help="Choose email subject"
            )
            
            email_type = st.radio("Email Format", ["HTML", "Text"])
        
        with col2:
            num_emails = st.slider(
                "Number of Emails",
                min_value=1,
                max_value=min(len(recipients), config.get('max_emails_per_day', 50)),
                value=min(3, len(recipients)),
                help="Number of emails to send"
            )
        
        # Preview
        if st.button("👁️ Preview Email", use_container_width=True):
            sample_recipient = recipients[0]
            if email_type == "HTML":
                preview_content = create_html_template(
                    sample_recipient.get('name', 'John Doe'),
                    sample_recipient.get('company', 'Tech Company'),
                    config['email']
                )
                st.markdown("**Email Preview:**")
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
                st.markdown("**Email Preview:**")
                st.text(preview_content)
        
        # Send emails
        if st.button("🚀 Start Sending", type="primary", use_container_width=True):
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
                        delay = random.randint(config.get('min_delay', 30), config.get('max_delay', 60))
                        time.sleep(delay)
                
                except Exception as e:
                    failed_count += 1
                    st.error(f"❌ Error sending to {recipient['email']}: {e}")
            
            # Final status
            progress_bar.progress(1.0)
            status_text.text("✅ Email sending completed!")
            
            st.success(f"📊 Results: {sent_count} sent, {failed_count} failed")
    
    with tab4:
        st.markdown('<h2 class="section-header">📊 Statistics</h2>', unsafe_allow_html=True)
        
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
            df_data = []
            for recipient in recipients:
                df_data.append({
                    'Email': recipient['email'],
                    'Name': recipient.get('name', '-'),
                    'Company': recipient.get('company', '-'),
                    'Added': recipient.get('added_date', '-')[:10] if recipient.get('added_date') else '-'
                })
            
            import pandas as pd
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
