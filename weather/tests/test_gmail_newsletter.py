import pytest
from django.core import mail
from django.utils import timezone

from weather.tasks import send_weather_email


@pytest.mark.django_db
def test_send_weather_email_task_via_smtp(
    subscription_with_user_and_city,
    settings,
    mocker,
):
    # Switching to the test backend
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    settings.DEFAULT_FROM_EMAIL = 'Weather Reminder <noreply@galkin.space>'

    # Mock OpenWeather
    fake_weather = {
        'temperature': 18.5,
        'humidity': 65,
        'wind_speed': 4.2,
        'wind_direction': 180,
        'weather_phenomena': 'clear',
        'timestamp': '2025-12-11 12:00',
    }
    mocker.patch('weather.openweather.OpenWeatherClient.get_weather', return_value=fake_weather)

    subscription = subscription_with_user_and_city

    # We run the task synchronously (not .delay())
    result = send_weather_email(subscription.pk)

    # 1. Check that the task returned the correct string.
    assert f'Email sent to {subscription.user.email}' in result

    # 2. Check that the email actually reached the outbox.
    assert len(mail.outbox) == 1
    sent_email = mail.outbox[0]

    # 3. Check the main fields of the letter
    assert sent_email.subject == f'Weather update for {subscription.city.city_name}'
    assert subscription.user.email in sent_email.to
    assert settings.DEFAULT_FROM_EMAIL == sent_email.from_email

    # 4. Check the contents of the email body
    body = sent_email.body
    assert 'Hello ' in body
    assert (
        subscription.user.first_name in body
        or subscription.user.username in body
        or 'friend' in body
    )

    assert 'Temperature: 18.5°C' in body
    assert 'Humidity: 65%' in body
    assert 'Wind: 4.2 m/s' in body
    assert 'Phenomena: clear' in body
    assert 'Good day!' in body

    # 5. Check that updated_at has been updated
    subscription.refresh_from_db()
    time_diff = timezone.now() - subscription.updated_at
    assert time_diff.total_seconds() < 5
