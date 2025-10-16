import os
import smtplib
from email.message import EmailMessage

# Email configuration from environment variables
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')

# Paths
HTML_PATH = os.environ.get('HTML_REPORT', 'report\\report.html')
JUNIT_XML_PATH = os.environ.get('JUNIT_XML', 'report\\junit.xml')

def send_email():
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = 'ST Jenkins CI Test Report'
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER  # Change to recipient if needed

    # Read HTML report as text
    if not os.path.exists(HTML_PATH):
        print(f"HTML report not found at {HTML_PATH}")
        return

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()
    msg.add_alternative(html, subtype='html')

    # Attach JUnit XML if available
    if os.path.exists(JUNIT_XML_PATH):
        with open(JUNIT_XML_PATH, 'rb') as f:
            xml_data = f.read()
        msg.add_attachment(xml_data, maintype='application', subtype='xml', filename='junit.xml')

    # Send email via SMTP
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print("✅ Test report email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    send_email()
