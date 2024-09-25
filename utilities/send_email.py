import smtplib
from email.message import EmailMessage
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

password = os.getenv('EMAIL_PASS')
email = "yohanvvinu@gmail.com"


def send_email(text, subject):
    email_message = EmailMessage()
    email_message["Subject"] = subject
    email_message.set_content(text)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(email, password)
    gmail.sendmail(email, email, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email("hi", "chicken")
