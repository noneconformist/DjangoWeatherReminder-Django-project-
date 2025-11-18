import pytest
from django.utils import timezone

from user_management.models import CustomUser
from weather.models import City, Subscription
from weather.tasks import send_weather_email


@pytest.mark.django_db
def test_celery_task_queue_and_execution(settings, subscription_with_user_and_city):
    # Enable eager mode for testing
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    # Console backend to avoid sending real emails.
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    sub = subscription_with_user_and_city

    # Launch Celery task
    result = send_weather_email.delay(sub.pk)

    # Check that the task is queued
    assert result.id is not None

    # Check that the task was completed successfully.
    result_output = result.get(timeout=10)  # wait up to 10 seconds
    assert 'Email sent' in result_output
