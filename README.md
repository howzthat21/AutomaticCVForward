# Gmail Email Sender Script

This Python script allows you to send emails using Gmail. It reads recipient email addresses from a `.txt` file and sends automated emails.

## Features
- Reads email addresses from a text file
- Sends automated emails via Gmail
- Supports customizable subject and body
- Uses `smtplib` for email sending
- Secure authentication using an App Password

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required libraries: `smtplib`, `ssl`

## Setup
### 1. Enable App Passwords in Gmail
To use this script, you need to enable [App Passwords](https://myaccount.google.com/apppasswords) in your Google account and generate a password. YOU NEED 2FA ENABLED IN YOUR GOOGLE ACCOUNT FOR THIS.

### 2. Install Dependencies
No additional dependencies are required beyond Python's standard library.

### 3. Prepare the Email List
Create a file named `emails.txt` with one email address per line:
```
example1@gmail.com
example2@gmail.com
```

### 4. Configure the Script
Update the script with your Gmail credentials:
```python
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
```

## Usage
Run the script using Python:
```sh
python script.py
```

## Security Note
- **Do not use your actual Gmail password**; always use an App Password.
- Ensure your email list (`emails.txt`) is kept private.


## Author
[Your Name]

