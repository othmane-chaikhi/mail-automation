# 📧 Email Automation Script

A Python script that sends personalized emails with human-like behavior to avoid spam filters. Perfect for sending job applications, CVs, or any bulk email campaigns.

## ✨ Features

- 🤖 **Human-like behavior**: Random delays (40-90 seconds) between emails
- 📝 **Personalized content**: Uses recipient names and company information
- 🎨 **Professional HTML emails**: Beautiful, responsive email templates
- 📊 **Progress tracking**: Resume from where you left off if interrupted
- 🔒 **Safe limits**: Built-in daily email limits to avoid spam
- 📋 **CSV integration**: Load recipients from a simple CSV file
- 🛡️ **Error handling**: Comprehensive logging and error recovery
- ⚙️ **Easy configuration**: Simple text-based configuration

## 🚀 Quick Start

### 1. Setup Gmail App Password

1. Go to your [Google Account settings](https://myaccount.google.com/)
2. Navigate to **Security** → **2-Step Verification** (enable if not already)
3. Go to **App passwords** and generate a new app password
4. Copy the 16-character password (you'll need this for `config.txt`)

### 2. Configure the Script

Edit `config.txt` with your information:

```txt
email=your_email@gmail.com
app_password=your_16_character_app_password
cv_path=your_cv_file.pdf
```

### 3. Add Recipients

Edit `recipients.csv` with your target emails:

```csv
email,name,company
hr@company1.com,John,Company 1
contact@company2.com,Jane,Company 2
```

### 4. Run the Script

**Option A: Double-click `send_cv.bat`** (Windows)
**Option B: Run directly** `python send_cv.py`

## 📁 File Structure

```
mailAutomation/
├── send_cv.py          # Main Python script
├── send_cv.bat         # Windows batch file for easy execution
├── config.txt          # Configuration file
├── recipients.csv      # List of email recipients
├── email_log.txt       # Log file (created automatically)
└── README.md          # This file
```

## ⚙️ Configuration Options

### config.txt Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `email` | Your Gmail address | Required |
| `app_password` | Gmail App Password | Required |
| `cv_path` | Path to your CV file | `CV_Othmane_Chaikhi.pdf` |
| `recipients_file` | CSV file with recipients | `recipients.csv` |
| `min_delay` | Minimum delay between emails (seconds) | `40` |
| `max_delay` | Maximum delay between emails (seconds) | `90` |
| `max_emails_per_day` | Daily email limit | `30` |

### recipients.csv Format

```csv
email,name,company
recipient1@example.com,John Doe,Company A
recipient2@example.com,Jane Smith,Company B
```

## 🎯 Email Features

### Random Subject Lines
The script automatically uses one of these subject lines:
- "Demande de stage PFE – Développement Web"
- "Candidature pour stage PFE - Développement Web"
- "Proposition de stage PFE - Développement Web"
- "Candidature spontanée - Stage PFE Développement"
- "Demande de stage - Développement Web Full Stack"

### Professional HTML Template
- Responsive design that works on all email clients
- Professional styling with your branding
- Both HTML and plain text versions
- Automatic CV attachment

### Human-like Behavior
- Random delays between emails (40-90 seconds)
- Random greeting variations
- Natural email flow
- Resume capability if interrupted

## 📊 Monitoring & Logs

### Log Files
- `email_log.txt`: Detailed log of all activities
- `email_progress.txt`: Progress tracking

### Log Information
- ✅ Successful sends
- ❌ Failed sends with error details
- ⏳ Timing information
- 📊 Final statistics

## 🛡️ Safety Features

### Spam Prevention
- **Daily limits**: Maximum 30 emails per day (configurable)
- **Human timing**: Random delays between emails
- **Professional content**: Well-formatted, personalized emails
- **Gmail compliance**: Uses proper SMTP authentication

### Error Handling
- **Connection issues**: Automatic retry logic
- **Invalid emails**: Skip and continue with next
- **Interruption**: Save progress and resume later
- **Validation**: Check all files before starting

## 🔧 Troubleshooting

### Common Issues

**"Authentication failed"**
- Check your Gmail App Password (not your regular password)
- Ensure 2-Factor Authentication is enabled
- Verify the email address in config.txt

**"File not found"**
- Check that `recipients.csv` exists
- Verify CV file path in config.txt
- Ensure all files are in the same directory

**"No recipients found"**
- Check CSV format (comma-separated)
- Ensure first row has headers: `email,name,company`
- Verify file encoding (UTF-8)

### Getting Help

1. Check `email_log.txt` for detailed error messages
2. Verify all configuration settings
3. Test with a small recipient list first
4. Ensure your Gmail account is in good standing

## 📈 Best Practices

### Email Volume
- **Start small**: Test with 5-10 emails first
- **Daily limits**: Stay under 30 emails per day
- **Spread out**: Don't send all emails at once

### Content Quality
- **Personalize**: Use recipient names and company info
- **Professional**: Keep content relevant and well-written
- **Attachments**: Only attach necessary files (CV, portfolio)

### Technical
- **Test first**: Always test with your own email
- **Monitor logs**: Check email_log.txt regularly
- **Backup**: Keep copies of your recipient lists

## 🚨 Important Notes

- **Gmail limits**: Free Gmail accounts have daily sending limits
- **Spam filters**: Even with this script, some emails may go to spam
- **Legal compliance**: Ensure you comply with email marketing laws
- **Professional use**: This is designed for legitimate business communications

## 📝 License

This script is provided as-is for educational and legitimate business purposes. Users are responsible for complying with all applicable laws and email service terms of service.

---

**Happy emailing! 📧✨**
