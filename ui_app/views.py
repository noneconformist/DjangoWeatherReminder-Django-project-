import logging

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from user_management.views import refresh_token

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
            token = request.session.get('access_token')
            print('Session keys:', request.session.keys())

            if not token:
                form.add_error(None, 'No access token found. Please log in again.')
                return render(request, 'subscription_add.html', {'form': form})

            headers = {'Authorization': f'Bearer {token}'}
            url = f'{settings.API_BASE_URL}/api/weather/?city={city}'

            try:
                response = requests.get(url, headers=headers, timeout=5)
            except requests.RequestException as e:
                logging.exception('Weather API request failed')
                form.add_error(None, f'API request failed: {e}')
                return render(request, 'subscription_add.html', {'form': form})

            if response.status_code == 401:
                new_token = refresh_token(request)
                if new_token:
                    headers = {'Authorization': f'Bearer {new_token}'}
                    response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                sub = form.save(commit=False)
                sub.user = request.user
                sub.save()
                return redirect('subscriptions_list')
            else:
                form.add_error('city', f'API error {response.status_code}: {response.text[:100]}')
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
