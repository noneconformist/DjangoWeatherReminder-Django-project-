from django import forms

from weather.models import City, Subscription


class SubscriptionForm(forms.ModelForm):
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Tokyo, Moscow, London, Paris...', 'class': 'form-control'}
        ),
    )

    class Meta:
        model = Subscription
        fields = ['city', 'notification_period']
        widgets = {
            'notification_period': forms.Select(
                choices=[
                    (1, 'Every hour'),
                    (3, 'Every 3 hours'),
                    (6, 'Every 6 hours'),
                ]
            )
        }

    def clean_city(self):
        city_name = self.cleaned_data['city'].strip().title()
        city, _ = City.objects.get_or_create(city_name=city_name)
        return city
