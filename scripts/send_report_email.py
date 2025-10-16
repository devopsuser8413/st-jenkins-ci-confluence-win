import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
TO_ADDR = os.environ.get('REPORT_TO', SMTP_USER)
HTML_PATH = os.environ.get('HTML_REPORT', 'report\\report.html')
SUBJECT = os.environ.get('EMAIL_SUBJECT', 'ST Jenkins CI Test Report')

def send_email():
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] = SMTP_USER
    msg['To'] = TO_ADDR

    with open(HTML_PATH, 'rb') as f:
        html = f.read()
    msg.set_content('Please view the HTML report attached.')
    msg.add_alternative(html, subtype='html')

    xml_path = os.environ.get('JUNIT_XML', 'report\\junit.xml')
    if os.path.exists(xml_path):
        with open(xml_path, 'rb') as f:
            xml = f.read()
        msg.add_attachment(xml, maintype='application', subtype='xml', filename='junit.xml')

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)

if __name__ == '__main__':
    send_email()
