from django.conf import settings
from django.db import models

INTERVAL_CHOICES = [
    (1, 'Every 1 hour'),
    (3, 'Every 3 hours'),
    (6, 'Every 6 hours'),
]


class UiSubscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ui_subscriptions'
    )
    city = models.CharField(max_length=100)
    interval = models.IntegerField(max_length=20, choices=INTERVAL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city} ({self.interval})'
