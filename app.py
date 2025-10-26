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
        greeting = self.get_random_greeting(name)
        company_sentence = (f" au sein de <strong>{company}</strong>" if company else "")
        
        # Get configurable template content
        template_config = self.config.get('template', {})
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
    
    def get_default_html_template(self) -> str:
        """Default HTML template."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
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
        </html>
        """
    
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
        greeting = self.get_random_greeting(name)
        company_sentence = (f" au sein de {company}" if company else "")
        
        # Get configurable template content
        template_config = self.config.get('template', {})
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
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📧 Email Settings", "📝 Template Editor", "📁 File Upload", "🚀 Send Emails"])
    
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
        
        # Template configuration
        template_config = {}
        
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
    
    with tab3:
        st.header("📁 File Upload")
        
        col1, col2 = st.columns(2)
        
        with col1:
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
        
        with col2:
            st.subheader("📋 Recipients CSV")
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
                    else:
                        st.error("No valid recipients found in CSV")
                        
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
                    recipients = []
            else:
                recipients = []
                st.warning("⚠️ Please upload recipients CSV")
    
    with tab4:
        st.header("🚀 Send Emails")
        
        # Check if all required fields are provided
        all_ready = (
            email and app_password and 
            cv_file is not None and 
            csv_file is not None and 
            len(recipients) > 0
        )
        
        if not all_ready:
            st.warning("⚠️ Please complete all required fields in the previous tabs before sending emails")
        else:
            # Validate email format
            if not validate_email(email):
                st.error("❌ Please enter a valid email address")
                all_ready = False
            
            # Check recipient count
            if len(recipients) > max_emails:
                st.warning(f"⚠️ You have {len(recipients)} recipients but limit is {max_emails}")
                if not st.checkbox("Continue anyway (not recommended)"):
                    all_ready = False
        
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
                    total_recipients = len(recipients)
                    
                    for i, recipient in enumerate(recipients):
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
