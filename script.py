import smtplib
import ssl
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#reads the file from the "userdetails.txt". Read the readme file first.
def load_user_details(filename="userdetails.txt"):
    with open(filename, "r") as file:
        lines = file.readlines()
        if len(lines)<2:
            print("not properly formated")
            sys.exit()
        return lines[0].strip(), lines[1].strip()

GMAIL_USER, GMAIL_PASSWORD = load_user_details()
print("credentials loaded")



#for now just add the resume in the same directory.
#will be updated at newer versions.
RESUME_PATH = "resume.pdf"

# Function to handle user input with a cancel option
def get_input(prompt):
    user_input = input(prompt)
    if user_input.lower() == "cancel":
        print("\n Script cancelled by user.")
        sys.exit()  
    return user_input

# Read email bodies from file
def load_email_templates(filename="email_templates.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().split("---")  

# Read recipient emails from file
def load_recipients(filename="emails.txt"):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]

#trying to make the code clean as possible sorry for this one.
default_subjects = [
    "{jobTitle} - {username}",
    "Application for {jobTitle}",
    "Interested in Opportunities at Your Company"
]

#array
default_bodies = load_email_templates()
recipients = load_recipients()

#custome input method
username = get_input("Enter your name (or type 'cancel' to exit): ")
contactNumber = get_input("Contact number  ")
jobTitle = get_input("What are you applying for? ")

# Choose a subject
print("\nChoose an email subject:")
for i, subject in enumerate(default_subjects, 1):
    print(f"{i}. {subject.format(username=username, jobTitle=jobTitle)}")
print("0. Write your own")
subject_choice = get_input("Enter choice (0-3): ")

if subject_choice == "0":
    subject = get_input("Enter your custom subject: ")
else:
    subject = default_subjects[int(subject_choice) - 1].format(username=username, jobTitle=jobTitle)

# Choose an email body
print("\nChoose an email body:")
for i in range(len(default_bodies)):
    print(f"{i+1}. Type {i+1}")
print("0. Write your own")
body_choice = get_input("Enter choice (0-3): ")

if body_choice == "0":
    print("Enter your custom email body (press Enter twice when done, or type 'cancel' to exit):")
    custom_body_lines = []
    while True:
        line = get_input("")
        if line == "":
            break
        custom_body_lines.append(line)
    body = "\n".join(custom_body_lines)
else:
    body = default_bodies[int(body_choice) - 1].strip().replace("[Your Name]", username)
    
# Add contact number to the email body
body += f"\n\nContact: {contactNumber}"

# Confirm before sending
print("\n Final Email Details:")
print(f" Subject: {subject}")
print(f" Body:\n{body}")
confirm = get_input("\nType 'send' to proceed, or 'cancel' to exit: ")
if confirm.lower() != "send":
    print(" Email sending aborted.")
    sys.exit()

# Setup SMTP connection
context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
server.login(GMAIL_USER, GMAIL_PASSWORD)

# Send emails with attachment
for recipient in recipients:
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach the resume
    with open(RESUME_PATH, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={RESUME_PATH}")
    msg.attach(part)

    # Send email
    try:
        server.sendmail(GMAIL_USER, recipient, msg.as_string())
        print(f" Email sent to {recipient}")
    except Exception as e:
        print(f" Failed to send email to {recipient}: {e}")

# Close the server
server.quit()
print("\n📧 All emails sent successfully!")
