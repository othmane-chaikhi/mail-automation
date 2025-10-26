# Email Automation Streamlit App

A web-based email automation tool for sending personalized job application emails with attachments.

## Features

- 🎯 **Personalized Emails**: Custom HTML and text templates with recipient personalization
- 📎 **File Attachments**: Upload and attach CV/PDF files to emails
- ⏱️ **Smart Timing**: Random delays between emails to appear more human-like
- 📊 **Progress Tracking**: Real-time progress bars and status updates
- 🔒 **Security**: Session-only credential storage, no persistent storage
- 📋 **CSV Import**: Upload recipient lists via CSV files
- 🛡️ **Safety Limits**: Configurable daily sending limits

## Quick Start

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Run the App**:
   ```bash
   streamlit run app.py
   ```

3. **Open in Browser**: The app will open at `http://localhost:8501`

### Deployment Options

#### Streamlit Cloud (Recommended)

1. **Push to GitHub**: Upload your code to a GitHub repository
2. **Deploy**: Go to [share.streamlit.io](https://share.streamlit.io) and connect your repository
3. **Configure**: Set up your deployment with the requirements file

#### Heroku

1. **Create Procfile**:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy Streamlit app"
   git push heroku main
   ```

## Usage Guide

### 1. Gmail Setup

- Enable 2-factor authentication on your Gmail account
- Generate an App Password (not your regular password)
- Use the App Password in the web interface

### 2. Prepare Your Files

**CV File**: Upload a PDF version of your CV

**Recipients CSV**: Create a CSV file with columns:
```csv
email,name,company
john@example.com,John Doe,Acme Corp
jane@example.com,Jane Smith,Tech Inc
```

### 3. Configure Settings

- **Timing**: Set min/max delays between emails (40-90 seconds recommended)
- **Limits**: Set daily email limits (30 emails recommended)
- **SMTP**: Uses Gmail SMTP settings (smtp.gmail.com:587)

### 4. Send Emails

- Click "Start Sending Emails" to begin the campaign
- Monitor progress with real-time updates
- Review results and statistics

## Security Features

- ✅ **No Persistent Storage**: Credentials are only stored in session memory
- ✅ **Input Validation**: Email format and file type validation
- ✅ **Rate Limiting**: Configurable sending limits
- ✅ **Error Handling**: Comprehensive error handling and logging

## Important Notes

⚠️ **Responsible Use**:
- Respect email laws and regulations (CAN-SPAM, GDPR, etc.)
- Don't exceed Gmail's sending limits (500 emails/day for regular accounts)
- Test with small batches first
- Use only for legitimate job applications

⚠️ **Gmail Limits**:
- Regular accounts: 500 emails/day
- Google Workspace: 2000 emails/day
- App passwords required for SMTP access

## Troubleshooting

### Common Issues

1. **SMTP Connection Failed**:
   - Verify Gmail credentials
   - Check if 2FA is enabled
   - Ensure App Password is correct

2. **CSV Upload Issues**:
   - Ensure CSV has proper headers (email, name, company)
   - Check for valid email addresses
   - Remove empty rows

3. **File Upload Problems**:
   - CV must be in PDF format
   - Check file size limits

### Support

For technical support, check the Streamlit documentation or create an issue in the repository.

## License

This project is for educational and personal use. Please use responsibly and in compliance with applicable laws and email service terms.
