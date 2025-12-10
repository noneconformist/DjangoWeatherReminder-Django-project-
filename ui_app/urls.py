from django.urls import path

from . import views

urlpatterns = [
    path('', views.subscriptions_list, name='subscriptions_list'),
    path('add/', views.subscription_add, name='subscription_add'),
    path('delete/<int:subscription_id>/', views.subscription_delete, name='subscription_delete'),
]
