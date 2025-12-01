from django.urls import path

from .views import CityListView, SubscriptionDetailView, subscription_list_create, weather_by_city

urlpatterns = [
    path('cities/', CityListView.as_view(), name='city-list'),
    path('subscriptions/', subscription_list_create, name='subscription-list-create'),
    path('subscriptions/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('', weather_by_city, name='weather-by-city'),
]
