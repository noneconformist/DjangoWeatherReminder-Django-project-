from rest_framework import serializers

from .models import City, Subscription


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_id', 'city_name', 'country']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Subscription
        fields = [
            'subscription_id',
            'user',
            'city',
            'notification_period',
            'created_at',
            'updated_at',
        ]

    def validate_notification_period(self, value):
        if value not in [1, 3, 6]:
            raise serializers.ValidationError('Notification period must be 1, 3, or 6 hours.')
        return value
