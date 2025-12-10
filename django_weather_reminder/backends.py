from django.core.mail.backends.base import BaseEmailBackend

from weather.sendpulse import SendPulseClient


class SendPulseEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        client = SendPulseClient()
        sent_count = 0

        for message in email_messages:
            payload = {
                'html': message.body.replace('\n', '<br>'),
                'text': message.body,
                'subject': message.subject,
                'from': {
                    'name': 'Django Weather Reminder',
                    'email': message.from_email or 'mogaxev854@kudimi.com',
                },
                'to': [{'name': addr.split('@')[0], 'email': addr} for addr in message.to],
            }

            try:
                result = client.send_email(payload)
                if result:
                    sent_count += 1
            except Exception as e:
                print(f'SendPulse error: {e}')

        return sent_count
