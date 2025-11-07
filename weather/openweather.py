from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone

OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'


def get_weather(city_name):
    params = {
        'q': city_name,
        'appid': settings.OPENWEATHER_API_KEY,
        'units': 'metric',
    }
    response = requests.get(OPENWEATHER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        timestamp = timezone.now()
        expired_at = timestamp + timedelta(hours=1)

        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind']['deg'],
            'weather_phenomena': data['weather'][0]['main'],  # example: "Rain", "Clear"
            'timestamp': timestamp.isoformat(),
            'expired_at': expired_at.isoformat(),
        }
    else:
        raise Exception(f'Weather API error: {response.status_code} → {response.text}')
