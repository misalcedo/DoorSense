from datetime import datetime


class StandardOutNotificationStrategy:
    @staticmethod
    def notify(subject, message, recipients):
        print({'subject': subject, 'message': message, 'recipients': recipients, 'time': datetime.now()})
