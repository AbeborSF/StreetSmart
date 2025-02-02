def send_email_alert(subject, recipient, message):
    msg = Message(subject, recipients=[recipient], body=message, sender='your-email@gmail.com')
    mail.send(msg)

def send_sms_alert(phone_number, message):
    client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=phone_number)
