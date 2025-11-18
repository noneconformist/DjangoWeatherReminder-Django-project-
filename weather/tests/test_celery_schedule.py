import pytest
from django_celery_beat.models import PeriodicTask

from user_management.models import CustomUser
from weather.models import City, Subscription


@pytest.mark.django_db
def test_subscription_creates_periodic_task(subscription_with_user_and_city):
    sub = subscription_with_user_and_city

    task = PeriodicTask.objects.get(name=f'subscription-{sub.pk}')
    assert task.task == 'weather.tasks.send_weather_email'
