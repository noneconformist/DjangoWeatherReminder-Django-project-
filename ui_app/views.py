import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SubscriptionForm
from .models import UiSubscription


@login_required
def subscriptions_list(request):
    subs = UiSubscription.objects.filter(user=request.user)
    return render(request, 'subscriptions_list.html', {'subscriptions': subs})


@login_required
def subscription_add(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            # Checking the city via OpenWeather
            api_key = settings.OPENWEATHER_API_KEY
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
            response = requests.get(url)

            if response.status_code == 200:
                sub = form.save(commit=False)
                sub.user = request.user
                sub.save()
                return redirect('subscriptions_list')
            else:
                form.add_error('city', 'Invalid city name for OpenWeather')
    else:
        form = SubscriptionForm()
    return render(request, 'subscription_add.html', {'form': form})


@login_required
def subscription_delete(request):
    subs = UiSubscription.objects.filter(user=request.user)
    if request.method == 'POST':
        sub_id = request.POST.get('subscription_id')
        UiSubscription.objects.filter(id=sub_id, user=request.user).delete()
        return redirect('subscriptions_list')
    return render(request, 'subscription_delete.html', {'subscriptions': subs})
