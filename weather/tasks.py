from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Subscription
from .openweather import OpenWeatherClient


@shared_task
def send_weather_email(subscription_id):
    """Send email to a specific subscription"""
    try:
        subscription = Subscription.objects.select_related('user', 'city').get(pk=subscription_id)
    except Subscription.DoesNotExist:
        return f'Subscription {subscription_id} not found'

    client = OpenWeatherClient(api_key=settings.OPENWEATHER_API_KEY)
    weather = client.get_weather(subscription.city.city_name)

    subject = f'Weather update for {subscription.city.city_name}'
    message = (
        f'Hello {subscription.user.full_name},\n\n'
        f'Temperature: {weather["temperature"]}°C\n'
        f'Humidity: {weather["humidity"]}%\n'
        f'Wind: {weather["wind_speed"]} m/s ({weather["wind_direction"]}°)\n'
        f'Phenomena: {weather["weather_phenomena"]}\n\n'
        f'Timestamp: {weather["timestamp"]}'
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [subscription.user.email],
        fail_silently=False,
    )

    # updating the last submission time
    subscription.updated_at = timezone.now()
    subscription.save(update_fields=['updated_at'])

    return f'Email sent to {subscription.user.email} for {subscription.city.city_name}'


@shared_task
def schedule_weather_notifications():
    """Check all subscriptions and send emails to those who are in their period"""
    now = timezone.now()
    subscriptions = Subscription.objects.select_related('user', 'city').all()

    sent_count = 0
    for sub in subscriptions:
        # difference between the current time and the last send
        elapsed_hours = (now - sub.updated_at).total_seconds() / 3600

        if elapsed_hours >= sub.notification_period:
            send_weather_email.delay(sub.pk)
            sent_count += 1

    return f'Scheduled {sent_count} notifications at {now.isoformat()}'
