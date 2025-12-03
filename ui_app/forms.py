from django import forms

from .models import UiSubscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = UiSubscription
        fields = ['city', 'interval']
