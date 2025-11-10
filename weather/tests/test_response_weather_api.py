import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_weather_api():
    client = APIClient()

    # Регистрация
    register_data = {
        'username': 'anton',
        'email': 'anton@example.com',
        'password': 'securepassword123',
        'first_name': 'Anton',
        'last_name': 'Galkin',
    }
    client.post('/register/', register_data, format='json')

    # Получение токена
    token_response = client.post(
        '/token/', {'username': 'anton', 'password': 'securepassword123'}, format='json'
    )
    access_token = token_response.data['access']

    # Запрос к API
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = client.get('/api/weather/?city=Tokyo')

    assert response.status_code == 200
    assert 'temperature' in response.data
