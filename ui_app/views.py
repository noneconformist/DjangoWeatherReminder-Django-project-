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
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            return redirect('subscriptions_list')
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
