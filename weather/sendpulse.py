import os

from django.conf import settings
from pysendpulse.pysendpulse import PySendPulse


class SendPulseClient:
    def __init__(self):
        token_dir = '/tmp/sendpulse_token_dir'
        os.makedirs(token_dir, exist_ok=True)
        token_file_path = os.path.join(token_dir, 'token_file')

        self.sp = PySendPulse(
            settings.SENDPULSE_API_ID,
            settings.SENDPULSE_API_SECRET,
            'FILE',
            token_file_path,
        )

    def create_list(self, name):
        try:
            return self.sp.create_addressbook(name)
        except Exception as e:
            return {'error': str(e)}

    def add_email(self, book_id, emails):
        # Many emails
        return self.sp.add_email_to_addressbook(book_id=book_id, emails=emails)

    def send_email(self, payload):
        return self.sp.smtp_send_mail(payload)
