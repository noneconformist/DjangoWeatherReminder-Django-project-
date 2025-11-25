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
                'email': {
                    'subject': message.subject,
                    'text': message.body,
                    'from': {
                        'name': 'MyApp',
                        'email': message.from_email,
                    },
                    'to': [{'email': addr} for addr in message.to],
                }
            }

            try:
                result = client.send_email(payload)
                if result:
                    sent_count += 1
            except Exception as e:
                print(f'SendPulse error: {e}')

        return sent_count
