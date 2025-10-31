from django.contrib.auth.views import LoginView
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import RegisterView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    # API endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
