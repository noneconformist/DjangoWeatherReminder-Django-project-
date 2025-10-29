from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import generics

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from .serializers import RegisterSerializer


def index(request):
    return render(request, 'users/index.html')


def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboard'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
