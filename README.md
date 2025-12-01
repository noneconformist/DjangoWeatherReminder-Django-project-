# Weather API with Authentication & Email Delivery



## Key Features

- User Registration – create accounts with username, email, and profile details (`/register/`).

- JWT Authentication – secure login with access and refresh tokens (`/token/`).

- Protected Weather Endpoint – query weather data by city (`/api/weather/?city=<CityName>`).

- Weather Data – includes temperature, humidity, wind speed/direction, and phenomena.

- Email Delivery – periodic weather reports sent to registered users via email.

- Task Scheduling – Celery workers handle background jobs for sending emails at defined intervals.

- SendPulse Integration – email messages are delivered through SendPulse SMTP API.

## Quick Start

### 1. Register a user

```
curl.exe -X POST http://127.0.0.1:8080/register/ `
  -H "Content-Type: application/json" `
  -d "{`"username`": `"anton`", `"email`": `"anton@example.com`", `"password`": `"securepassword123`"}"
```

### 2. Obtain tokens

```
curl.exe -X POST http://127.0.0.1:8080/token/ `
  -H "Content-Type: application/json" `
  -d "{`"username`": `"anton`", `"password`": `"securepassword123`"}"
```

### 3. Access weather data

```
curl.exe -X GET http://127.0.0.1:8080/api/weather/?city=Tokyo `
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
### 4. Example Response:

```
{
  "temperature": 19.85,
  "humidity": 31,
  "wind_speed": 7.2,
  "wind_direction": 350,
  "weather_phenomena": "Clear",
  "timestamp": "2025-11-07T06:42:34.393100+00:00",
  "expired_at": "2025-11-07T07:42:34.393100+00:00"
}
```

### 5. Receive scheduled emails

- After registration, users automatically receive weather updates via email.

- Celery workers run in the background and send reports at the configured interval (e.g., hourly, daily).

- SendPulse SMTP credentials must be configured in environment variables (e.g., SENDPULSE_USER, SENDPULSE_PASSWORD).


***

### Documentation
- Interactive API docs are available via:

- Swagger UI → http://127.0.0.1:8080/swagger

- ReDoc → http://127.0.0.1:8080/redoc

## Author
Anton Galkin

## License
This project is released under the MIT License.

## Project status
Study / Educational project.