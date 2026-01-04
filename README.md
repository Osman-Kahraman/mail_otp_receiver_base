# mail_otp_receiver_base

**mail_otp_receiver_base** is a **self-hosted disposable email (temp mail) system** built with **SendGrid Inbound Parse** and **Flask**.

It allows you to receive emails on your own domain, automatically extract **OTP / verification codes** from both HTML and plain-text emails, and forward them — along with attachments — to your main inbox, without exposing your real email address to spammy websites.

I built this mainly to avoid giving my personal email to random services.  
I’m also keeping this repo as a reminder for my future self — because I *will* forget how I set this up.

---

## Features

- **Self-Hosted Temp Mail** – Works like popular temporary email services  
- **OTP Extraction** – Automatically parses verification codes using regex  
- **HTML & Text Support** – Handles both email formats  
- **Attachment Forwarding** – Forwards attachments if present  
- **Custom Domain Support** – Full control via your own domain  
- **Lightweight & Simple** – Minimal setup, no database required  

---

## Requirements

You will need a **custom domain**.  
SendGrid Inbound Parse **does not work with free email providers**.  

I personally bought one from **Namecheap for about $2/year**.

You also need a SendGrid account with:

- Inbound Parse enabled  
- Domain authentication completed  
- MX records pointing to SendGrid  

Additionally:

- Python 3.9+  
- Flask  

---

## Installation

Clone the repository and navigate into the project directory:

```sh
git clone https://github.com/Osman-Kahraman/mail_otp_receiver_base.git
cd mail_otp_receiver_base
pip install -r requirements.txt
```

---

## Configuration

Update the following values in your Flask app:

```py
from_email = 'noreply@your-domain.com'
to_email = 'YOUR_EMAIL'
API = 'YOUR_SENDGRID_API_KEY'
```

Make sure your SendGrid Inbound Parse webhook points to:

```sh
POST /email
```

---

## How It Works

Incoming emails are received by SendGrid via MX records.
Your server is not responsible for email delivery.

Once an email arrives:
	•	SendGrid forwards the email payload to your Flask app
	•	HTML or plain-text content is parsed
	•	OTP / verification codes are extracted
	•	Attachments are preserved
	•	Everything is forwarded to your main inbox

If your server is asleep (for example on free-tier hosting), nothing breaks.
Parsing simply happens when the server wakes up.

---

## Deployment

This project works well on Render on the free tier.

Since email delivery is handled entirely by SendGrid, your server only performs post-processing.
Sleeping servers are not a problem — emails don’t wait, and they don’t bounce.

---

## Disclaimer

This project is intended for personal use and experimentation.
Do not use it for malicious purposes or to bypass service terms.

---

## License

MIT License
