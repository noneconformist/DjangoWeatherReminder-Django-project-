from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from weather.models import Subscription

from .forms import SubscriptionForm


def subscriptions_list(request):
    subscriptions = Subscription.objects.filter(user=request.user).select_related('city')
    return render(request, 'subscriptions_list.html', {'subscriptions': subscriptions})


@login_required
def subscription_add(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()

            return redirect('subscriptions_list')
    else:
        form = SubscriptionForm()

    return render(request, 'subscription_add.html', {'form': form})


@login_required
def subscription_delete(request, subscription_id):
    subscription = Subscription.objects.filter(
        subscription_id=subscription_id, user=request.user
    ).first()

    if request.method == 'POST' and subscription:
        subscription.delete()
        return redirect('subscriptions_list')

    return render(request, 'subscription_delete.html', {'subscription': subscription})
