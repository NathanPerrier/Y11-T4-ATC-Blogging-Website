import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

GMAIL_SECRET_KEY = 'tlwzdvpfotedwjdi'

def create_email(name, recipient_email, subject, message):
    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = 'Ambrose Treacy College'
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Add the message to the body of the email
        with open('email.html', 'r') as file:
            email_template = file.read()
        
        # Replace placeholders in the email template with actual values
        email_template = email_template.replace('{{subject}}', subject)
        email_template = email_template.replace('{{message}}', message)
        
        with open('atc-logo.png', 'rb') as logo_file:
            logo_content = logo_file.read()

        logo_mime = MIMEImage(logo_content)
        logo_mime.add_header('Content-ID', '<logo>')
        msg.attach(logo_mime)

        # Embed the logo in the HTML content
        email_template = email_template.replace('{{logo}}', '<img src="cid:logo" alt="Logo">')
        
        msg.attach(MIMEText(email_template, 'html'))

        return msg.as_string()
    
    except Exception as e:
        print('An error occurred while creating the email:', str(e))

def send_email(from_email, to_email, message):
    try:
        # Create a secure SSL/TLS connection with the SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        server.login(from_email, GMAIL_SECRET_KEY)

        # Send the email
        server.sendmail(from_email, to_email, message)
        
        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))
    finally:
        server.quit()

class Email():
    def __init__(self):
        pass
        
    def send_contact_us_emails(self, name, recipient_email, subject, message, admin_email='contact.webgenieai@gmail.com'):
        
        user_subject = 'Thanks ' + name + ' For Contacting Us!'
        user_message = create_email(name, recipient_email, user_subject, 'We will get back to you soon! If you have any more enquiries feel free to contat us again.')
        send_email(admin_email, recipient_email, user_message)
        
        admin_subject = 'Contact Us Message'
        admin_message = create_email(name, admin_email, admin_subject, 'Name: ' + name + '<br><br>Email: ' + recipient_email + '<br><br>Subject: ' + subject + '<br><br>Message: ' + message)
        send_email(admin_email, 'nathanperrier138@gmail.com', admin_message)


