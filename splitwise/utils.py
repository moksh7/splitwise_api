import os
from threading import Thread
from django.core.mail import EmailMessage

from splitwise.models import SplitUser


class EmailThread(Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.message = message
        Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.message, os.getenv('EMAIL_HOST_USER'), self.recipient_list)
        msg.content_subtype = "html"
        resp = msg.send()

def send_html_mail(subject, body, debtor_id, lender_id=None):
    if lender_id and debtor_id:
        lender = SplitUser.objects.filter(id=lender_id).first()
        lender = lender.name if lender else None
        debtor = SplitUser.objects.filter(id=debtor_id).first()
        debtor = debtor.name if debtor else None
        body = body % lender
    EmailThread(subject, body, [debtor.email]).start()