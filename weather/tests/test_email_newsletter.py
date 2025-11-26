import pytest

from weather.tasks import send_weather_email


@pytest.mark.django_db
def test_send_weather_email_task(subscription_with_user_and_city, settings, monkeypatch):
    settings.EMAIL_BACKEND = 'django_weather_reminder.backends.SendPulseEmailBackend'
    settings.DEFAULT_FROM_EMAIL = 'test@django_weather_reminder.com'

    called = []

    class FakeSendPulseBackend:
        def __init__(self, *args, **kwargs):
            # Accept any arguments from Django
            pass

        def send_messages(self, email_messages):
            message = email_messages[0]
            payload = {
                'email': {
                    'subject': message.subject,
                    'text': message.body,
                    'html': message.body
                    if getattr(message, 'content_subtype', '') == 'html'
                    else None,
                    'to': [{'email': addr} for addr in message.to],
                    'from': {'email': message.from_email},
                }
            }
            called.append(payload)
            return len(email_messages)  # Django expects the number of messages sent

    # Patch the exactly class
    monkeypatch.setattr(
        'django_weather_reminder.backends.SendPulseEmailBackend', FakeSendPulseBackend
    )

    subscription = subscription_with_user_and_city
    result = send_weather_email(subscription.pk)

    # Checking the task result
    assert f'Email sent to {subscription.user.email}' in result

    # Check that send_messages was called
    assert len(called) == 1
    payload = called[0]['email']

    assert subscription.city.city_name in payload['subject']
    assert f'Hello {subscription.user.first_name}' in (payload['text'] or '')
    assert subscription.user.email in [item['email'] for item in payload['to']]
