from flask import Flask, request
from bs4 import BeautifulSoup
import re, base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

from_email = 'noreply@your-domain.com'
to_email = 'YOUR_EMAIL'
API = 'YOUR_API_KEY'

app = Flask(__name__)
otp = ''
_to = ''
sg = SendGridAPIClient(API)

@app.route('/email', methods=['POST'])
def email_receiver():
    global otp, sg, _to

    print('From:', request.form['from'])
    print('To:', request.form['to'])
    print('Subject:', request.form['subject'])
    
    if 'html' in request.form:
        soup = BeautifulSoup(request.form['html'], 'html.parser')
        text = soup.get_text()

        if "Your verification code is as mentioned below" in text:
            match = re.search(r'verification code.*?(\d{6})', text)
            _to = request.form['to']
            otp = match.group(1)

    elif 'text' in request.form:
        text = request.form['text']
        if "Verification Code:" in text:
            match = re.search(r'\b\d{4}\b', text)

        _to = request.form['to']
        otp = match.group() if match else ""

    attachments = []
    for file_key in request.files.keys():
        file = request.files[file_key]
        file_bytes = file.read()
        encoded = base64.b64encode(file_bytes).decode("utf-8")

        attachment = Attachment(
            FileContent(encoded),
            FileName(file.filename),
            FileType(file.content_type),
            Disposition('attachment')
        )

        attachments.append(attachment)

    message = Mail(from_email = from_email, to_emails = to_email, subject = request.form['to'], plain_text_content = text)
    for attachment in attachments:
        message.add_attachment(attachment)
    
    sg.send(message)

    return 'OK', 200
