import pytest

from user_management.models import CustomUser
from weather.models import City, Subscription
from weather.tasks import schedule_weather_notifications


@pytest.mark.django_db
def test_celery_beat_periodicity(settings):
    # Enable eager mode for testing
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    # Simulate multiple Celery Beat launches
    results = [schedule_weather_notifications.delay().get() for _ in range(3)]

    # Check that the task is executed every time
    assert all('Scheduled' in str(r) for r in results)
