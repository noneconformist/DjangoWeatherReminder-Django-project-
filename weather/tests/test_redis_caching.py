import pytest

from weather.openweather import OpenWeatherClient


@pytest.mark.django_db
def test_weather_cache(mocker):
    # Clear Redis
    import redis

    r = redis.Redis.from_url('redis://redis:6379/1')
    r.flushdb()

    # API fake response
    fake_resp = mocker.MagicMock()
    fake_resp.status_code = 200
    fake_resp.ok = True
    fake_resp.json.return_value = {
        'main': {'temp': 20.0, 'humidity': 65},
        'weather': [{'main': 'Clear'}],
        'wind': {'speed': 3.5, 'deg': 180},
        'name': 'Tokyo',
    }
    fake_resp.raise_for_status = lambda: None

    fake_session = mocker.MagicMock()
    fake_session.get.return_value = fake_resp

    # Mock before creating a client
    mocker.patch('requests.Session', return_value=fake_session)

    # Create client
    client = OpenWeatherClient(api_key='test')

    # First call
    result1 = client.get_weather('Tokyo')
    assert result1['temperature'] == 20.0

    # Second call from cache
    result2 = client.get_weather('Tokyo')
    assert result2['temperature'] == 20.0
    assert result1 == result2

    # The API is called once
    fake_session.get.assert_called_once()
