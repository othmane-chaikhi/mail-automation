#!/usr/bin/env python3
"""
Email Automation Script - Human-like Email Sender
Sends personalized emails with random delays and variations to avoid spam filters.
"""

import smtplib
import csv
import time
import random
import logging
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EmailAutomation:
    def __init__(self, config_file: str = "config.txt"):
        """Initialize the email automation with configuration."""
        self.config = self.load_config(config_file)
        self.server = None
        self.sent_count = 0
        self.failed_count = 0
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from file."""
        config = {
            'email': '',
            'app_password': '',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'cv_path': 'CV_Othmane_Chaikhi.pdf',
            'recipients_file': 'recipients.csv',
            'min_delay': 40,
            'max_delay': 90,
            'max_emails_per_day': 30
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config[key.strip()] = value.strip()
        
        return config
    
    def get_random_subject(self) -> str:
        """Get a random subject line variation."""
        subjects = [
            "Candidature pour un stage PFE – Développement web / IA / Data / Testing",
            "Candidature stage PFE - Développement web / IA / Data / Testing",
            "Candidature pour stage PFE - Technologies numériques",
            "Candidature spontanée - Stage PFE Développement / IA / Data",
            "Candidature pour un stage PFE - Développement et Intelligence Artificielle"
        ]
        return random.choice(subjects)
    
    def get_random_greeting(self, name: str) -> str:
        """Get a consistent greeting for personalized feel."""
        return f"Bonjour {name},"
    
    def create_html_email(self, name: str, company: str) -> str:
        """Create a professional HTML email template."""
        greeting = self.get_random_greeting(name)
        
        html_content = f"""
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
                    
                    <p>Je me permets de vous contacter afin de vous présenter ma candidature pour un stage de fin d'études (PFE) en développement web, intelligence artificielle, data ou testing au sein de <strong>{company}</strong>.</p>
                    
                    <div class="highlight">
                        <p><strong>Je m'appelle Othmane Chaikhi</strong>, étudiant en cycle ingénieur en Informatique et Réseaux (MIAGE) à l'EMSI Rabat (2023–2026).</p>
                        <p>Passionné par le développement et les technologies émergentes, j'ai réalisé plusieurs projets académiques et freelances, notamment :</p>
                        <ul>
                            <li>une application e-commerce complète (Django, SEO) pour une coopérative marocaine,</li>
                            <li>un tableau de bord RH (Power BI, analyse de données),</li>
                            <li>des applications web avec Spring Boot, Java EE et Django,</li>
                            <li>et des projets d'IA utilisant Python, machine learning et visualisation de données.</li>
                        </ul>
                    </div>
                    
                    <p>Mon objectif est de mettre en pratique mes compétences techniques, d'apprendre auprès de professionnels expérimentés et de contribuer à vos projets innovants dans le domaine du numérique.</p>
                    
                    <p>Vous trouverez ci-joint mon CV, que j'espère retiendra votre attention.<br>
                    Je serais honoré de pouvoir échanger avec vous au sujet de cette opportunité de stage.</p>
                    
                    <p>Je vous remercie sincèrement pour votre temps et votre considération.</p>
                </div>
                
                <div class="footer">
                    <div class="signature">
                        <p><strong>Bien cordialement,</strong><br>
                        <strong>Othmane Chaikhi</strong><br>
                        📞 +212 631-889579<br>
                        📧 {self.config['email']}</p>
                        <p>🔗 <a href="https://othmanechaikhi.page.gd" target="_blank">https://othmanechaikhi.page.gd</a></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def create_text_email(self, name: str, company: str) -> str:
        """Create a plain text email template."""
        greeting = self.get_random_greeting(name)
        
        text_content = f"""
{greeting}

Je me permets de vous contacter afin de vous présenter ma candidature pour un stage de fin d'études (PFE) en développement web, intelligence artificielle, data ou testing au sein de {company}.

Je m'appelle Othmane Chaikhi, étudiant en cycle ingénieur en Informatique et Réseaux (MIAGE) à l'EMSI Rabat (2023–2026).
Passionné par le développement et les technologies émergentes, j'ai réalisé plusieurs projets académiques et freelances, notamment :

- une application e-commerce complète (Django, SEO) pour une coopérative marocaine,
- un tableau de bord RH (Power BI, analyse de données),
- des applications web avec Spring Boot, Java EE et Django,
- et des projets d'IA utilisant Python, machine learning et visualisation de données.

Mon objectif est de mettre en pratique mes compétences techniques, d'apprendre auprès de professionnels expérimentés et de contribuer à vos projets innovants dans le domaine du numérique.

Vous trouverez ci-joint mon CV, que j'espère retiendra votre attention.
Je serais honoré de pouvoir échanger avec vous au sujet de cette opportunité de stage.

Je vous remercie sincèrement pour votre temps et votre considération.

Bien cordialement,
Othmane Chaikhi
📞 +212 631-889579
📧 {self.config['email']}

🔗 https://othmanechaikhi.page.gd
        """
        return text_content.strip()
    
    def connect_smtp(self) -> bool:
        """Connect to SMTP server."""
        try:
            self.server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            self.server.starttls()
            self.server.login(self.config['email'], self.config['app_password'])
            logger.info("SUCCESS: Connected to SMTP server successfully")
            return True
        except Exception as e:
            logger.error(f"ERROR: Failed to connect to SMTP: {e}")
            return False
    
    def send_email(self, recipient: Dict) -> bool:
        """Send a single email to a recipient."""
        try:
            # Create main message container
            msg = MIMEMultipart('mixed')
            msg['From'] = self.config['email']
            msg['To'] = recipient['email']
            msg['Subject'] = self.get_random_subject()
            
            # Create alternative container for text and HTML
            alternative = MIMEMultipart('alternative')
            
            # Create text and HTML versions
            text_content = self.create_text_email(recipient['name'], recipient['company'])
            html_content = self.create_html_email(recipient['name'], recipient['company'])
            
            # Attach both versions to alternative container
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')
            
            alternative.attach(text_part)
            alternative.attach(html_part)
            
            # Attach the alternative container to main message
            msg.attach(alternative)
            
            # Attach CV if it exists
            if os.path.exists(self.config['cv_path']):
                with open(self.config['cv_path'], "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(self.config["cv_path"])}'
                    )
                    msg.attach(part)
            else:
                logger.warning(f"WARNING: CV file not found: {self.config['cv_path']}")
            
            # Send email
            self.server.send_message(msg)
            self.sent_count += 1
            logger.info(f"SUCCESS: Email sent to {recipient['email']} ({recipient['name']})")
            return True
            
        except Exception as e:
            self.failed_count += 1
            logger.error(f"ERROR: Failed to send to {recipient['email']}: {e}")
            return False
    
    def load_recipients(self) -> List[Dict]:
        """Load recipients from CSV file."""
        recipients = []
        try:
            with open(self.config['recipients_file'], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    recipients.append(row)
            logger.info(f"Loaded {len(recipients)} recipients")
        except FileNotFoundError:
            logger.error(f"ERROR: Recipients file not found: {self.config['recipients_file']}")
        except Exception as e:
            logger.error(f"ERROR: Error loading recipients: {e}")
        
        return recipients
    
    def save_progress(self, recipients: List[Dict], start_index: int):
        """Save progress to resume later if needed."""
        progress_file = "email_progress.txt"
        with open(progress_file, 'w') as f:
            f.write(f"last_sent_index={start_index}\n")
            f.write(f"sent_count={self.sent_count}\n")
            f.write(f"failed_count={self.failed_count}\n")
            f.write(f"timestamp={datetime.now().isoformat()}\n")
    
    def load_progress(self) -> int:
        """Load progress from previous run."""
        progress_file = "email_progress.txt"
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                for line in f:
                    if line.startswith('last_sent_index='):
                        return int(line.split('=')[1])
        return 0
    
    def run(self):
        """Main execution function."""
        logger.info("Starting email automation...")
        
        # Check if we should continue from previous run
        start_index = self.load_progress()
        if start_index > 0:
            response = input(f"Found previous progress at index {start_index}. Continue? (y/n): ")
            if response.lower() != 'y':
                start_index = 0
        
        # Connect to SMTP
        if not self.connect_smtp():
            return
        
        # Load recipients
        recipients = self.load_recipients()
        if not recipients:
            logger.error("ERROR: No recipients found")
            return
        
        # Check daily limit
        max_emails = int(self.config['max_emails_per_day'])
        if len(recipients) > max_emails:
            logger.warning(f"WARNING: You have {len(recipients)} recipients but daily limit is {max_emails}")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return
        
        try:
            # Send emails
            for i, recipient in enumerate(recipients[start_index:], start=start_index):
                logger.info(f"Processing {i+1}/{len(recipients)}: {recipient['email']}")
                
                # Send email
                success = self.send_email(recipient)
                
                # Save progress every 5 emails
                if (i + 1) % 5 == 0:
                    self.save_progress(recipients, i + 1)
                
                # Random delay between emails (human-like behavior)
                if i < len(recipients) - 1:  # Don't delay after last email
                    delay = random.randint(
                        int(self.config['min_delay']), 
                        int(self.config['max_delay'])
                    )
                    logger.info(f"Waiting {delay}s before next email...")
                    time.sleep(delay)
            
            # Final summary
            logger.info(f"Campaign completed!")
            logger.info(f"Sent: {self.sent_count}, Failed: {self.failed_count}")
            
            # Clean up progress file
            if os.path.exists("email_progress.txt"):
                os.remove("email_progress.txt")
                
        except KeyboardInterrupt:
            logger.info("Campaign interrupted by user")
            self.save_progress(recipients, start_index + self.sent_count)
        except Exception as e:
            logger.error(f"ERROR: Unexpected error: {e}")
        finally:
            if self.server:
                self.server.quit()
                logger.info("Disconnected from SMTP server")

def main():
    """Main entry point."""
    print("Email Automation Script")
    print("=" * 50)
    
    # Check if config file exists
    if not os.path.exists("config.txt"):
        print("WARNING: Configuration file 'config.txt' not found!")
        print("Please create it with your email settings.")
        return
    
    # Run automation
    automation = EmailAutomation()
    automation.run()

if __name__ == "__main__":
    main()
