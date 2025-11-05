import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from user_management.models import CustomUser
from weather.models import City, Subscription


@pytest.mark.django_db
def test_create_subscription():
    # Creating a user
    user = CustomUser.objects.create_user(
        username='anton', email='anton@example.com', password='securepass123'
    )

    # Creating a city
    city = City.objects.create(city_name='Tokyo', country='Japan')

    # Authorization
    client = APIClient()
    client.force_authenticate(user=user)

    # Request to create a subscription
    url = reverse('subscription-list-create')
    payload = {'city': city.city_id, 'notification_period': 3}
    response = client.post(url, payload, format='json')

    # Checking
    assert response.status_code == 201
    data = response.json()
    assert data['city'] == city.city_id
    assert data['notification_period'] == 3

    # Check in the database
    assert Subscription.objects.filter(user=user, city=city).exists()
