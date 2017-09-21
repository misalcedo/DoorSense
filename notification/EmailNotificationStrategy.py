from email.mime.text import MIMEText
from smtplib import SMTP

from notification.EmailConfiguration import RASPBERRY_PI_BOT

_COMMA_SPACE = ", "


class EmailNotificationStrategy:
    def __init__(self, email_configuration=RASPBERRY_PI_BOT):
        self.email_configuration = email_configuration

    def notify(self, subject, message, recipients):
        email = MIMEText(message, _charset="UTF-8")
        email['From'] = self.email_configuration.from_email
        email['To'] = _COMMA_SPACE.join(recipients)
        email['Subject'] = subject

        with SMTP(host=self.email_configuration.host,
                  port=self.email_configuration.port,
                  timeout=self.email_configuration.timeout) as smtp:
            smtp.starttls()
            smtp.login(user=self.email_configuration.user, password=self.email_configuration.password)
            smtp.send_message(email)
