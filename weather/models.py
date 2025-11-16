import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from user_management.models import CustomUser


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.city_name}, {self.country}'


class Subscription(models.Model):
    PERIOD_CHOICES = [
        (1, 'Every 1 hour'),
        (3, 'Every 3 hours'),
        (6, 'Every 6 hours'),
    ]

    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='subscriptions')
    notification_period = models.IntegerField(choices=PERIOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} → {self.city.city_name} ({self.notification_period}h)'


# Subscription periodic task
def create_subscription_task(subscription):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=subscription.notification_period,
        period=IntervalSchedule.HOURS,
    )
    PeriodicTask.objects.update_or_create(
        name=f'subscription-{subscription.pk}',
        defaults={
            'interval': schedule,
            'task': 'weather.tasks.send_weather_email',
            'args': json.dumps([subscription.pk]),
        },
    )


@receiver(post_save, sender=Subscription)
def subscription_post_save(sender, instance, created, **kwargs):
    if created:
        create_subscription_task(instance)
