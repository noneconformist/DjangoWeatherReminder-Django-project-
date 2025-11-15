import json
from datetime import timedelta

import redis
import requests
from django.utils import timezone


class OpenWeatherClient:
    OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

    def __init__(self, api_key, redis_url='redis://redis:6379/1'):
        self.api_key = api_key
        self.session = requests.Session()
        self.redis = redis.Redis.from_url(redis_url)

    def get_weather(self, city_name):
        # Check data in cache
        cache_key = f'weather:{city_name.lower()}'
        cached_data = self.redis.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

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

        openweather_response = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind']['deg'],
            'weather_phenomena': data['weather'][0]['main'],  # example: "Rain", "Clear"
            'timestamp': timestamp.isoformat(),
            'expired_at': expired_at.isoformat(),
        }

        # save in Redis for 30 minutes
        self.redis.setex(cache_key, 60 * 15, json.dumps(openweather_response))

        return openweather_response
