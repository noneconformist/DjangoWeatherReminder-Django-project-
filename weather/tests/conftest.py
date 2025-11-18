import pytest
from django.utils import timezone

from user_management.models import CustomUser
from weather.models import City, Subscription


@pytest.fixture
def subscription_with_user_and_city(db):
    user = CustomUser.objects.create_user(
        username='anton',
        email='anton@example.com',
        password='securepassword123',
        first_name='Anton',
        last_name='Galkin',
    )
    city = City.objects.create(city_name='Tokyo', country='Japan')
    sub = Subscription.objects.create(
        user=user,
        city=city,
        notification_period=1,
        created_at=timezone.now(),
        updated_at=timezone.now(),
    )
    return sub
