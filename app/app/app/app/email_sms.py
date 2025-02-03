from flask_mail import Message
from app import mail
from twilio.rest import Client

def send_email(subject, recipient, message):
    msg = Message(subject, recipients=[recipient])
    msg.body = message
    mail.send(msg)

def send_sms(phone_number, message):
    account_sid = 'your_twilio_sid'
    auth_token = 'your_twilio_auth_token'
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_='your_twilio_number', to=phone_number)