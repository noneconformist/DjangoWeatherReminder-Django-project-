from datetime import timedelta

import requests
from django.utils import timezone


class OpenWeatherClient:
    OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()

    def get_weather(self, city_name):
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric',
        }
        response = self.session.get(self.OPENWEATHER_API_URL, params=params)
        response.raise_for_status()
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
