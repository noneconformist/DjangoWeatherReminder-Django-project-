from django.contrib.auth.views import LoginView
from django.urls import include, path

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
]
