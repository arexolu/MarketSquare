from flask_mail import Mail, Message

mailer = Mail()

def send_message(send_to: str, subject: str, message: str, reply_to = None):
    msg = Message(subject,
        sender='no-reply@sendgrid.ultractiv.com',
        recipients=[send_to],
        reply_to=reply_to
    )
    msg.body = message
    msg.html = message
    mailer.send(msg)