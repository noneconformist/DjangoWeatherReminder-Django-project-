import pytest
from django.core import mail

from weather.tasks import send_weather_email


@pytest.mark.django_db
def test_send_weather_email_task(subscription_with_user_and_city, settings):
    # Using a test email backend
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    settings.DEFAULT_FROM_EMAIL = 'test@example.com'

    # Subscription from the fixture
    subscription = subscription_with_user_and_city

    # Run the task directly (without Celery delay)
    result = send_weather_email(subscription.pk)

    # Check that the email has reached the outbox.
    assert len(mail.outbox) == 1
    email = mail.outbox[0]

    # Checking the contents of the letter
    assert f'Weather update for {subscription.city.city_name}' in email.subject
    assert f'Hello {subscription.user.first_name}' in email.body
    assert email.to == [subscription.user.email]

    # Check that the task returned the correct result.
    assert f'Email sent to {subscription.user.email}' in result
