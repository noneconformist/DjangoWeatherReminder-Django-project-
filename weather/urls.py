from django.urls import path

from .views import CityListView, SubscriptionDetailView, SubscriptionListCreateView

urlpatterns = [
    path('cities/', CityListView.as_view(), name='city-list'),
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'),
    path('subscriptions/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription-detail'),
]
