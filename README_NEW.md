# 📧 Email Automation Pro

A modern, robust email automation system built with Streamlit and Python. Send personalized emails to multiple recipients with professional templates and advanced features.

## ✨ Features

- 🔐 **Secure Gmail Integration** - Uses App Passwords for secure authentication
- 📧 **Professional Templates** - HTML and text email templates
- 👥 **Recipient Management** - Add, remove, and manage email recipients
- 📊 **Statistics Dashboard** - Track your email campaigns
- ⚙️ **Easy Configuration** - Simple JSON-based configuration
- 🎨 **Modern UI** - Clean, responsive interface
- 📎 **Attachment Support** - Send CVs and other attachments
- ⏱️ **Smart Delays** - Configurable delays between emails
- 🔄 **Bulk Import** - Import recipients from CSV files

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_new.txt
```

### 2. Configure Gmail

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Click "App passwords"
   - Generate a new 16-character password
3. Update `email_config.json` with your credentials

### 3. Run the App

```bash
python run_app.py
```

Or directly with Streamlit:

```bash
streamlit run app_new.py
```

## 📁 File Structure

```
email-automation/
├── app_new.py              # Main application
├── run_app.py              # Launcher script
├── requirements_new.txt    # Dependencies
├── email_config.json       # Configuration file
├── recipients.json         # Recipients database
├── README_NEW.md          # This file
└── CV_Othmane_Chaikhi.pdf # Your CV (optional)
```

## ⚙️ Configuration

Edit `email_config.json` to customize:

```json
{
  "email": "your.email@gmail.com",
  "app_password": "your_16_char_app_password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "min_delay": 30,
  "max_delay": 60,
  "max_emails_per_day": 50,
  "subjects": [
    "Your subject lines here"
  ]
}
```

## 👥 Managing Recipients

### Add Recipients Manually
1. Go to the "Recipients" tab
2. Fill in email, name, and company
3. Click "Add Recipient"

### Import from CSV
1. Create a CSV with columns: `email`, `name`, `company`
2. Upload in the "Recipients" tab
3. Recipients will be automatically added

### Example CSV Format
```csv
email,name,company
john@company.com,John Doe,Tech Company
jane@startup.io,Jane Smith,Startup Inc
```

## 📧 Sending Emails

1. **Configure Settings** - Set up Gmail credentials
2. **Add Recipients** - Import or add email addresses
3. **Choose Template** - Select HTML or text format
4. **Preview** - See how your email will look
5. **Send** - Start the email campaign

## 🛡️ Security Features

- **App Passwords Only** - No regular passwords stored
- **Local Storage** - All data stored locally
- **No External Services** - Direct SMTP connection
- **Configurable Limits** - Set daily email limits

## 🔧 Troubleshooting

### Gmail Authentication Issues

1. **Enable 2FA**: Make sure 2-Factor Authentication is enabled
2. **Generate App Password**: Create a new 16-character App Password
3. **Check Credentials**: Verify email and password in config
4. **Test Connection**: Use the "Test Gmail Connection" button

### Common Errors

- **"Username and Password not accepted"**: Check App Password
- **"Connection refused"**: Check internet connection
- **"Authentication failed"**: Verify 2FA is enabled

## 📊 Features Overview

### Configuration Tab
- Gmail settings (email, app password)
- SMTP configuration
- Timing settings (delays between emails)
- Safety limits (max emails per day)

### Recipients Tab
- Add recipients manually
- Bulk import from CSV
- View and manage recipient list
- Remove recipients

### Send Emails Tab
- Choose email template (HTML/Text)
- Preview emails before sending
- Configure sending parameters
- Monitor sending progress

### Statistics Tab
- View recipient count
- Track unique companies
- Monitor app status

## 🎨 Customization

### Email Templates
Edit the `EmailTemplate` class in `app_new.py` to customize:
- Email content
- Styling (HTML templates)
- Signature information
- Company-specific content

### Configuration
Modify `email_config.json` for:
- Default settings
- Subject lines
- Timing parameters
- Safety limits

## 📝 License

This project is for educational and personal use. Please respect email etiquette and anti-spam laws.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your Gmail configuration
3. Ensure all dependencies are installed

## 🔄 Updates

This is a clean rebuild of the email automation system with:
- ✅ Simplified architecture
- ✅ Better error handling
- ✅ Modern UI design
- ✅ Robust configuration management
- ✅ Clean code structure

---

**Happy Email Automation! 📧✨**
