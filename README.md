# 📧 Email Automation Pro

A professional, modern email automation system built with Python and Streamlit. Send personalized emails to multiple recipients with beautiful templates and advanced features.

## ✨ Features

### 🔐 **Secure Email Integration**
- **Multiple Providers**: Gmail, Outlook, Yahoo, Custom SMTP
- **App Password Support**: Secure authentication for Gmail
- **Connection Testing**: Test your email configuration before sending
- **Robust Error Handling**: Clear error messages and troubleshooting

### 📧 **Professional Email System**
- **Beautiful Templates**: HTML and text email templates
- **Attachment Support**: Send CVs and documents
- **Smart Delays**: Configurable timing between emails
- **Preview Function**: See emails before sending
- **Multiple Subjects**: Rotate between different subject lines

### 👥 **Advanced Recipient Management**
- **Manual Addition**: Add recipients one by one
- **CSV Import**: Bulk import from spreadsheets
- **Recipient Database**: Persistent storage with metadata
- **Easy Management**: View, edit, delete recipients
- **Company Tracking**: Track unique companies and positions

### 📊 **Analytics & Statistics**
- **Real-time Metrics**: Track recipients, companies, templates
- **Sending Statistics**: Monitor email campaign results
- **Company Distribution**: Visualize recipient distribution
- **Contact History**: Track when recipients were last contacted

### 🎨 **Modern User Interface**
- **Responsive Design**: Works on desktop and mobile
- **Professional Styling**: Clean, modern interface
- **Tabbed Navigation**: Organized sections
- **Real-time Feedback**: Progress tracking and status updates
- **Dark/Light Theme**: Automatic theme detection

## 🚀 Quick Start

### 1. **Installation**

```bash
# Clone or download the project
git clone <repository-url>
cd email-automation

# Install dependencies
pip install -r requirements.txt
```

### 2. **Launch Application**

```bash
# Simple launcher (recommended)
python launch.py

# Or directly with Streamlit
streamlit run email_automation.py
```

### 3. **Configure Email**

1. **Go to Configuration Tab**
2. **Select Email Provider** (Gmail, Outlook, Yahoo, Custom)
3. **Enter Email Address** and Password/App Password
4. **Test Connection** to verify settings
5. **Save Configuration**

### 4. **Add Recipients**

1. **Go to Recipients Tab**
2. **Add Manually** or **Import CSV**
3. **View and Manage** your recipient list

### 5. **Send Emails**

1. **Go to Send Emails Tab**
2. **Choose Template** and Subject
3. **Preview Email** before sending
4. **Start Sending** your campaign

## 📁 Project Structure

```
email-automation/
├── email_automation.py    # Main application
├── launch.py             # Simple launcher
├── requirements.txt      # Dependencies
├── README.md            # This file
├── config.json          # Configuration (auto-created)
├── recipients.json      # Recipients database (auto-created)
├── templates.json       # Email templates (auto-created)
└── CV_Othmane_Chaikhi.pdf # Your CV (optional)
```

## ⚙️ Configuration

### **Email Providers**

| Provider | SMTP Server | Port | Security |
|----------|-------------|------|----------|
| Gmail | smtp.gmail.com | 587 | TLS |
| Outlook | smtp-mail.outlook.com | 587 | TLS |
| Yahoo | smtp.mail.yahoo.com | 587 | TLS |
| Custom | Your server | Your port | Your choice |

### **Gmail Setup**

1. **Enable 2-Factor Authentication**
2. **Generate App Password**:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Click "App passwords"
   - Generate a new 16-character password
3. **Use App Password** (not your regular password)

### **Configuration File**

The app automatically creates `config.json`:

```json
{
  "email": "your.email@gmail.com",
  "password": "your_app_password",
  "provider": "gmail",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "min_delay": 30,
  "max_delay": 60,
  "max_emails_per_day": 50,
  "subjects": ["Subject 1", "Subject 2"],
  "greetings": ["Bonjour", "Salut"]
}
```

## 👥 Managing Recipients

### **Manual Addition**

1. Go to **Recipients Tab**
2. Fill in the form:
   - **Email**: Required
   - **Name**: Optional
   - **Company**: Optional
   - **Position**: Optional
   - **Notes**: Optional
3. Click **Add Recipient**

### **CSV Import**

Create a CSV with these columns:
```csv
email,name,company,position,notes
john@company.com,John Doe,Tech Company,HR Manager,Interested in AI
jane@startup.io,Jane Smith,Startup Inc,CTO,Looking for developers
```

### **Recipient Management**

- **View All**: See all recipients in expandable cards
- **Edit**: Click edit button to modify recipient info
- **Delete**: Remove recipients you no longer need
- **Status Tracking**: Track when recipients were last contacted

## 📧 Email Templates

### **Default Template**

The app includes a professional HTML template with:
- **Modern Design**: Clean, responsive layout
- **Personalization**: Name, company, email placeholders
- **Professional Content**: Stage PFE application content
- **Contact Information**: Your details and portfolio

### **Template Variables**

- `{name}`: Recipient's name
- `{company}`: Recipient's company
- `{email}`: Your email address

### **Custom Templates**

You can create custom templates by modifying the `TemplateManager` class.

## 📊 Statistics & Analytics

### **Real-time Metrics**

- **Total Recipients**: Number of people in your database
- **Unique Companies**: Number of different companies
- **Email Templates**: Number of available templates
- **App Status**: Current application status

### **Detailed Analytics**

- **Recipients Overview**: Complete list with metadata
- **Company Distribution**: Bar chart of company distribution
- **Contact History**: Track when recipients were contacted
- **Sending Results**: Success/failure rates

## 🛡️ Security Features

### **Data Protection**

- **Local Storage**: All data stored locally on your machine
- **No External Services**: Direct SMTP connection only
- **Encrypted Passwords**: Passwords stored securely
- **Session Management**: Secure session handling

### **Email Safety**

- **Rate Limiting**: Configurable delays between emails
- **Daily Limits**: Maximum emails per day
- **Error Handling**: Graceful failure handling
- **Connection Testing**: Verify settings before sending

## 🔧 Troubleshooting

### **Common Issues**

#### **Gmail Authentication Failed**
1. **Check 2FA**: Ensure 2-Factor Authentication is enabled
2. **App Password**: Use 16-character App Password, not regular password
3. **Wait Time**: New App Passwords can take 5-10 minutes to activate
4. **Test Connection**: Use the test button to verify

#### **Connection Refused**
1. **Internet**: Check your internet connection
2. **Firewall**: Ensure SMTP ports are not blocked
3. **Provider Settings**: Verify SMTP server and port
4. **Credentials**: Double-check email and password

#### **Emails Not Sending**
1. **Recipients**: Ensure you have recipients added
2. **Configuration**: Check your email configuration
3. **Templates**: Verify email templates are loaded
4. **Attachments**: Check attachment file paths

### **Debug Information**

The app provides debug information in the Configuration tab:
- **Config File Email**: What's loaded from config
- **Form Email**: What's in the form fields
- **Connection Details**: SMTP server and port being used

## 🚀 Advanced Features

### **Multiple Email Providers**

Switch between different email providers:
- **Gmail**: Most popular, requires App Password
- **Outlook**: Microsoft's email service
- **Yahoo**: Yahoo Mail support
- **Custom**: Your own SMTP server

### **Smart Email Scheduling**

- **Random Delays**: Prevents spam detection
- **Configurable Timing**: Set min/max delays
- **Daily Limits**: Control sending volume
- **Progress Tracking**: Real-time sending status

### **Professional Templates**

- **HTML Format**: Beautiful, responsive emails
- **Text Format**: Plain text fallback
- **Personalization**: Dynamic content insertion
- **Professional Design**: Modern, clean layout

## 📈 Performance

### **Optimizations**

- **Efficient Data Storage**: JSON-based persistence
- **Lazy Loading**: Load data only when needed
- **Connection Pooling**: Reuse SMTP connections
- **Memory Management**: Clean up resources properly

### **Scalability**

- **Large Recipient Lists**: Handle thousands of recipients
- **Batch Processing**: Send emails in batches
- **Error Recovery**: Continue after failures
- **Progress Tracking**: Monitor long-running operations

## 🤝 Support

### **Getting Help**

1. **Check Troubleshooting**: Review common issues
2. **Debug Information**: Use the debug section
3. **Test Connection**: Verify your email settings
4. **Check Logs**: Look for error messages

### **Best Practices**

1. **Test First**: Always test with a small batch
2. **Use Delays**: Don't send emails too quickly
3. **Monitor Results**: Check success/failure rates
4. **Keep Updated**: Update recipients regularly

## 🔄 Updates

### **Version History**

- **v2.0**: Complete rebuild with modern architecture
- **v1.0**: Initial version with basic features

### **Future Features**

- **Email Scheduling**: Send emails at specific times
- **A/B Testing**: Test different email versions
- **Analytics Dashboard**: Advanced reporting
- **API Integration**: Connect with other tools

## 📝 License

This project is for educational and personal use. Please respect email etiquette and anti-spam laws.

---

**Happy Email Automation! 📧✨**

*Built with ❤️ using Python and Streamlit*