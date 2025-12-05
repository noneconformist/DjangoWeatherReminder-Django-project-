import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
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
            return redirect(reverse('index'))
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


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Obtaining a token upon login
        url = f'{settings.API_BASE_URL}/token/'
        api_response = requests.post(url, json={'username': username, 'password': password})

        if api_response.status_code == 200:
            tokens = api_response.json()
            print('Tokens received:', tokens)  # temporary for check

            request = self.request
            # Save tokens in the session
            request.session['access_token'] = tokens.get('access')
            request.session['refresh_token'] = tokens.get('refresh')
            request.session.modified = True

        return response


def refresh_token(request):
    refresh = request.session.get('refresh_token')
    if not refresh:
        return None

    url = f'{settings.API_BASE_URL}/token/refresh/'
    response = requests.post(url, json={'refresh': refresh})
    if response.status_code == 200:
        new_access = response.json()['access']
        request.session['access_token'] = new_access
        return new_access
    return None
