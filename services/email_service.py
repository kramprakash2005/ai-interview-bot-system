import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)


def send_invite_email(to_email, link, title, desc):

    print("SMTP CONFIG:", SMTP_HOST, SMTP_PORT, SMTP_USER)

    msg = MIMEMultipart("alternative")

    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = f"AI Interview Invitation – {title}"


    # ---------------- TEXT VERSION ----------------

    text = f"""
Hello,

I am Tachibana Hinata, your AI Interviewer.

You have been invited to an AI-powered interview session.

Position: {title}

Start here:
{link}

Note:
This link can be used only once.

Good luck.
"""


    # ---------------- HTML VERSION ----------------

    html = f"""
<html>
<body style="font-family:Segoe UI,Arial,sans-serif;background:#eef1f7;padding:20px;">

<div style="
max-width:620px;
margin:auto;
background:white;
border-radius:14px;
overflow:hidden;
box-shadow:0 6px 18px rgba(0,0,0,0.15);
">

<!-- HEADER -->

<div style="
background:linear-gradient(90deg,#6366f1,#8b5cf6);
color:white;
padding:22px;
text-align:center;
font-size:22px;
font-weight:bold;
letter-spacing:1px;
">

AI Interview System

</div>


<!-- BODY -->

<div style="padding:28px;">


<p style="font-size:15px;">Hello,</p>


<p style="font-size:15px;line-height:1.6;">

I am <b>Tachibana Hinata</b>, your AI Interviewer for this session.

You have been selected to participate in an interactive AI-driven interview.
This interview will evaluate your skills, experience, and problem-solving ability
in real time.

</p>


<div style="
background:#f3f4ff;
border-left:6px solid #6366f1;
padding:16px;
border-radius:8px;
margin-top:18px;
">

<p style="margin:0;font-size:16px;">
<b>Interview Role:</b> {title}
</p>

</div>



<p style="margin-top:22px;font-size:14px;line-height:1.6;">

Before starting, please ensure:

• Stable internet connection  
• Working microphone / headset  
• Quiet environment  

When you are ready, begin the interview below.

</p>



<div style="text-align:center;margin:30px;">

<a href="{link}"
style="
background:#ec4899;
color:white;
padding:14px 28px;
text-decoration:none;
border-radius:10px;
font-size:16px;
font-weight:bold;
box-shadow:0 4px 10px rgba(236,72,153,0.4);
display:inline-block;
">

Start Interview

</a>

</div>



<p style="font-size:12px;color:#666;">

This interview link is personal and can be used only once.
If the button does not work, copy the link below:

</p>


<p style="
font-size:12px;
word-break:break-all;
color:#111;
">

{link}

</p>



<p style="margin-top:24px;font-size:14px;">

I will be guiding you through the interview.

Stay confident.

<br><br>

<b>— Tachibana Hinata</b>  
AI Interviewer

</p>


</div>


<!-- FOOTER -->

<div style="
background:#f1f1f1;
padding:12px;
text-align:center;
font-size:12px;
color:#555;
">

AI Interview Platform • Automated Assessment System

</div>


</div>

</body>
</html>
"""

    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))


    # ---------------- SMTP SEND ----------------

    try:

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as s:

            s.ehlo()
            s.starttls()
            s.ehlo()

            if SMTP_USER and SMTP_PASS:
                s.login(SMTP_USER, SMTP_PASS)

            s.send_message(msg)

        print("EMAIL SENT SUCCESS")

    except Exception as e:

        print("EMAIL ERROR:", type(e).__name__, e)

def send_otp_email(to_email, otp):

    msg = MIMEMultipart("alternative")

    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Your Login Code – AI Interview Platform"


    text = f"""
Your OTP code is: {otp}
This code will expire soon.
"""


    html = f"""
<html>
<body style="font-family:Segoe UI,Arial,sans-serif;background:#eef1f7;padding:20px;">

<div style="
max-width:620px;
margin:auto;
background:white;
border-radius:14px;
overflow:hidden;
box-shadow:0 6px 18px rgba(0,0,0,0.15);
">

<!-- HEADER -->

<div style="
background:linear-gradient(90deg,#6366f1,#8b5cf6);
color:white;
padding:22px;
text-align:center;
font-size:22px;
font-weight:bold;
letter-spacing:1px;
">

AI Interview Platform

</div>


<!-- BODY -->

<div style="padding:28px;">

<p style="font-size:15px;">Hello,</p>


<p style="font-size:15px;line-height:1.6;">

You are trying to sign in to the <b>AI Interview Platform</b>.

Use the verification code below to continue.

</p>


<div style="
background:#f3f4ff;
border-left:6px solid #6366f1;
padding:16px;
border-radius:8px;
margin-top:18px;
text-align:center;
">

<p style="margin:0;font-size:14px;color:#444;">
Your One-Time Password
</p>

<h1 style="
margin-top:10px;
font-size:36px;
letter-spacing:6px;
color:#111;
">
{otp}
</h1>

</div>



<p style="margin-top:22px;font-size:14px;line-height:1.6;">

This code will expire shortly.

If you did not request this login, you can ignore this email.

</p>



<p style="margin-top:24px;font-size:14px;">

Stay confident.

<br><br>

<b>— Tachibana Hinata</b>  
AI Interviewer

</p>


</div>


<!-- FOOTER -->

<div style="
background:#f1f1f1;
padding:12px;
text-align:center;
font-size:12px;
color:#555;
">

AI Interview Platform • Secure Login System

</div>


</div>

</body>
</html>
"""

    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))


    try:

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as s:

            s.ehlo()
            s.starttls()
            s.ehlo()

            if SMTP_USER and SMTP_PASS:
                s.login(SMTP_USER, SMTP_PASS)

            s.send_message(msg)

        print("OTP EMAIL SENT")

    except Exception as e:

        print("OTP EMAIL ERROR:", e)