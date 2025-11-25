import pytest
from pysendpulse.pysendpulse import PySendPulse

from weather.tasks import send_weather_email


@pytest.mark.django_db
def test_send_weather_email_task(subscription_with_user_and_city, settings, monkeypatch):
    # Using a test email backend
    settings.EMAIL_BACKEND = 'django_weather_reminder.backends.SendPulseEmailBackend'
    settings.DEFAULT_FROM_EMAIL = 'test@django_weather_reminder.com'

    called = {}

    def fake_smtp_send_mail(self, payload):
        called['payload'] = payload
        return True

    # Mocking the send_email method
    monkeypatch.setattr(PySendPulse, 'smtp_send_mail', fake_smtp_send_mail)

    # Subscription from the fixture
    subscription = subscription_with_user_and_city

    # Run the task directly (without Celery delay)
    result = send_weather_email(subscription.pk)

    # Check that the task returned the correct result.
    assert f'Email sent to {subscription.user.email}' in result
    assert 'payload' in called
    payload = called['payload']['email']

    # Проверяем содержимое payload
    assert f'Weather update for {subscription.city.city_name}' in payload.get('subject', '')
    assert f'Hello {subscription.user.first_name}' in payload.get('text', '')
    assert subscription.user.email in [addr['email'] for addr in payload.get('to', [])]
