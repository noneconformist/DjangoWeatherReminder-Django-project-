import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from user_management.models import CustomUser


@pytest.mark.django_db
def test_register_and_get_jwt_token():
    client = APIClient()

    # 1. Registration
    register_url = reverse('register')
    user_data = {
        'username': 'anton',
        'email': 'anton@example.com',
        'password': 'securepassword123',
        'first_name': 'Anton',
        'last_name': 'Galkin',
    }

    response = client.post(register_url, user_data, format='json')
    assert response.status_code == 201
    assert CustomUser.objects.filter(username='anton').exists()

    # 2. Obtaining a token
    token_url = reverse('token_obtain_pair')
    token_data = {'username': 'anton', 'password': 'securepassword123'}

    response = client.post(token_url, token_data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
