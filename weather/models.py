from django.db import models

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
